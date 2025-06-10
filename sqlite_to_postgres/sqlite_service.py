import logging
import sqlite3
from contextlib import contextmanager
from typing import Any, Generator, Optional

import sqlite_to_postgres.config as config


class SQLiteService:
    """Установление соединения с SQLite и получение данных."""

    @contextmanager
    def connection_context(
        self, db_path: str
    ) -> Generator[sqlite3.Connection, Any, None]:
        """Контекстный менеджер подключения к бд."""
        try:
            connection = sqlite3.connect(db_path)
            connection.row_factory = sqlite3.Row
            yield connection
        except sqlite3.Error as e:
            logging.error(
                f'Не удалось подключиться к базe sqlite: {e}'
            )
        finally:
            connection.close()

    @staticmethod
    def get_data_from_table(
        connection: sqlite3.Connection,
        table_name: str
    ) -> Generator[Any, Any, None]:
        """Получение данных из таблицы."""
        cursor = connection.cursor()
        cursor.execute(f'SELECT * FROM {table_name}')
        while rows := cursor.fetchmany(config.BATCH_SIZE):
            yield rows

    @staticmethod
    def get_count_data(
        connection: sqlite3.Connection,
        table_name: str
    ) -> Optional[int]:
        """Получение количества строк из таблицы Sqlite."""
        cursor = connection.cursor()
        try:
            cursor.execute(f'SELECT count(*) FROM {table_name}')
            row = cursor.fetchone()
            return row[0]
        except sqlite3.Error as e:
            logging.error(
                f'Не удалось получить строки из таблицы {table_name}: {e}'
            )
