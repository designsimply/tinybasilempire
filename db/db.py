import os
import psycopg2
import psycopg2.extras


def get_db_connection():
    """Database connection."""
    conn = psycopg2.connect(
        host="localhost",
        database="stuffdb",
        # TDDO move these variables to config. config.DB_USERNAME
        # any os.environ should be in config
        user=os.environ["DB_USERNAME"],
        password=os.environ["DB_PASSWORD"],
    )
    return conn


# do all the sql!
def query_db(sql, params=None):
    cursor_factory = psycopg2.extras.NamedTupleCursor
    with get_db_connection() as conn:
        conn.autocommit = True
        with conn.cursor(cursor_factory=cursor_factory) as cur:
            cur.execute(sql, params)
            try:
                return list(cur.fetchall())
            except psycopg2.ProgrammingError:
                return []
