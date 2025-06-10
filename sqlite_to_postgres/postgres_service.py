import logging
from contextlib import contextmanager
from typing import Any, Generator, Optional

import sqlite_to_postgres.config as config
import psycopg2
import psycopg2.extras
from psycopg2 import sql


class PostgresService:
    """Установление соединения с Postgres и вставка данных."""

    @contextmanager
    def connection_context(
        self,
        dsn: dict
    ) -> Generator[psycopg2.connect, Any, None]:
        """Менеджер контекста подключения к бд."""
        try:
            connection = psycopg2.connect(**dsn)
            yield connection
        except (Exception, psycopg2.DatabaseError) as e:
            logging.error(
                f'Не удалось подключиться к базe postgres: {e}'
            )
        finally:
            connection.close()

    @staticmethod
    def data_to_postgres(
        connection: psycopg2.connect,
        table_name: str,
        column_names_str: str,
        data: Any
    ) -> None:
        """Запись данных в таблицу Postgres."""
        cursor = connection.cursor()
        query = (
            f'INSERT INTO {table_name} ({column_names_str}) '
            'VALUES %s ON CONFLICT (id) DO NOTHING'
        )
        psycopg2.extras.execute_values(cursor, query, data)
        connection.commit()

    @staticmethod
    def get_data_from_postgres(
        connection: psycopg2.connect,
        table: str,
    ) -> Generator[Any, Any, None]:
        """Получение данных из таблицы Postgres."""
        cur = connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor
        )
        try:
            cur.execute(
                sql.SQL(
                    'SELECT * FROM {}').format(
                        sql.Identifier(table)
                    )
            )
            while rows := cur.fetchmany(config.BATCH_SIZE):
                yield rows
        except (Exception, psycopg2.DatabaseError) as e:
            logging.error(e)

    @staticmethod
    def get_count_data(
        connection: psycopg2.connect,
        table: str,
    ) -> Optional[int]:
        """Получение количества строк из таблицы Postgres."""
        cur = connection.cursor()
        try:
            cur.execute(
                sql.SQL(
                    'SELECT count(*) FROM {}'
                ).format(sql.Identifier(table))
            )
            row = cur.fetchone()
            return row[0]
        except (Exception, psycopg2.DatabaseError) as e:
            logging.error(e)
