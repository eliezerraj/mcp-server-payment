import psycopg_pool
from contextlib import contextmanager

class DatabasePool:
    """Singleton-like connection pool for PostgreSQL"""

    _pool = None

    @classmethod
    def initialize(cls, 
                   conninfo: str, 
                   min_size: int = 1, 
                   max_size: int = 10, 
                   timeout: int = 30):
        if cls._pool is None:
            cls._pool = psycopg_pool.ConnectionPool(
                conninfo,
                min_size=min_size,
                max_size=max_size,
                timeout=timeout,
            )

    @classmethod
    @contextmanager
    def get_connection(cls):
        if cls._pool is None:
            raise RuntimeError("DatabasePool not initialized. Call initialize() first.")
        with cls._pool.connection() as conn:
            yield conn