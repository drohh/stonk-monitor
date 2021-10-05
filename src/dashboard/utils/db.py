from contextlib import contextmanager
import psycopg2
from dataclasses import dataclass

@dataclass
class DBConnInfo:
    db: str
    user: str
    password: str
    host: str
    port: int = 5432


class WarehouseConnection:
    def __init__(self, db_conn_info: DBConnInfo):
        self.db_conn_info = db_conn_info
        self.conn_url = (
            f'postgresql://{db_conn_info.user}:{db_conn_info.password}@'
            f'{db_conn_info.host}:{db_conn_info.port}/{db_conn_info.db}'
        )
        print(f'Connected to database via {self.conn_url}')

    @contextmanager
    def managed_cursor(self, cursor_factory=None):
        self.conn = psycopg2.connect(dbname=self.db_conn_info.db,
                                    user=self.db_conn_info.user,
                                    password=self.db_conn_info.password,
                                    host=self.db_conn_info.host,
                                    port=self.db_conn_info.port)
        self.conn.autocommit = True
        self.cur = self.conn.cursor(cursor_factory=cursor_factory)
        try:
            yield self.cur
        finally:
            self.cur.close()
            self.conn.close()
