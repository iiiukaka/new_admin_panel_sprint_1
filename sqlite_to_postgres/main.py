import logging
import sqlite3
from dataclasses import astuple, fields
from typing import Any, Optional, Sequence

import psycopg2

import sqlite_to_postgres.config as config
from sqlite_to_postgres.postgres_service import PostgresService
from sqlite_to_postgres.sqlite_service import SQLiteService

logging.basicConfig(level=logging.INFO)


def load_from_sqlite(
        sqlite_connection: sqlite3.Connection,
        postgres_connection: psycopg2.connect
        ) -> None:
    """Основной метод загрузки данных из SQLite в Postgres."""
    mapping_table = config.MAPPING_TABLE
    for table, model in mapping_table.items():
        is_imported = True
        try:
            data_generator = sqlite_service.get_data_from_table(
                sqlite_connection,
                table
            )
            for rows in data_generator:
                data_to_insert, column_names_str = reformat_data(model, rows)
                postgres_service.data_to_postgres(
                    postgres_connection,
                    table,
                    column_names_str,
                    data_to_insert,
                )
        except (sqlite3.Error, psycopg2.DatabaseError) as e:
            logging.error(f'Не удалось забрать данные из таблицы {table}: {e}')
            is_imported = False

        if is_imported:
            logging.info(f'Данные из таблицы {table} успешно загружены')


def reformat_data(
        model: str,
        data: Sequence
) -> Optional[tuple[list[tuple[Any, ...]], str]]:
    """Подготовка данных для вставки."""
    try:
        data_from_db = [(model(**row)) for row in data]
        data_to_insert = [astuple(item) for item in data_from_db]
        column_names = [field.name for field in fields(data_from_db[0])]
        column_names_str = ', '.join(column_names)
        return data_to_insert, column_names_str
    except Exception as e:
        logging.error(e)


if __name__ == '__main__':
    sqlite_service = SQLiteService()
    postgres_service = PostgresService()
    with sqlite_service.connection_context(
        config.SQLITE_DB_PATH
    ) as s_conn, postgres_service.connection_context(
        config.POSTGRES_DB_DSN
    ) as p_conn:
        load_from_sqlite(s_conn, p_conn)
