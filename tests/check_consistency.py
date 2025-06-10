import logging
import sqlite3
from dataclasses import astuple
from typing import Any, Generator

import psycopg2

from sqlite_to_postgres.config import (
    MAPPING_TABLE,
    POSTGRES_DB_DSN,
    SQLITE_DB_PATH,
)
from sqlite_to_postgres.postgres_service import PostgresService
from sqlite_to_postgres.sqlite_service import SQLiteService

logging.basicConfig(level=logging.INFO)


def compare_data(
        sqlite_connection: sqlite3.Connection,
        postgres_connection: psycopg2.connect
) -> None:
    """Метод сравнения данных из SQLite и  Postgres."""
    mapping_table = MAPPING_TABLE
    success = True
    for table, model in mapping_table.items():
        count_rows_sqlite = sqlite_service.get_count_data(
            sqlite_connection, table
        )
        count_rows_postgres = postgres_service.get_count_data(
            postgres_connection, table
        )
        try:
            assert count_rows_sqlite == count_rows_postgres
        except AssertionError:
            logging.error(f'Количество строк не совпадает в таблице {table}')
            success = False

        part_data_sqlite = get_all_from_table_sqlite(
            sqlite_connection, table, model
        )

        part_data_postgres = get_data_postgres(
            postgres_connection, table, model
        )

        try:
            for batch_sqlite, batch_postgres in zip(
                part_data_sqlite, part_data_postgres
            ):
                assert batch_sqlite == batch_postgres
        except AssertionError:
            logging.error(f'Данные не совпадают в таблице {table}')
            success = False
    if success:
        logging.info('Все данные сопоставлены, различий нет')


def get_all_from_table_sqlite(
        sqlite_connection: sqlite3.Connection,
        table: str,
        model: str
) -> Generator[list[tuple[Any, ...]], Any, None]:
    """Получение данных из SQLite."""
    sqlite_data_generator = sqlite_service.get_data_from_table(
        sqlite_connection, table
    )
    for rows in sqlite_data_generator:
        data_from_db = [model(**row).cut_date() for row in rows]
        yield reformat_data(data_from_db)


def get_data_postgres(
        postgres_connection: psycopg2.connect,
        table: str,
        model: str
) -> Generator[list[tuple[Any, ...]], Any, None]:
    """Получение данных из Postgres."""
    postgres_data_generator = postgres_service.get_data_from_postgres(
        postgres_connection, table
    )
    for rows in postgres_data_generator:
        data_from_db = [model(**row).post_init() for row in rows]
        yield reformat_data(data_from_db)


def reformat_data(
        data_from_db: list[Any]
) -> list[tuple[Any, ...]]:
    """Подготовка данных."""
    return sorted([astuple(item) for item in data_from_db])


if __name__ == '__main__':
    sqlite_service = SQLiteService()
    postgres_service = PostgresService()
    with sqlite_service.connection_context(
        SQLITE_DB_PATH
    ) as sqlite_conn, postgres_service.connection_context(
        POSTGRES_DB_DSN
    ) as pg_conn:
        compare_data(sqlite_conn, pg_conn)
