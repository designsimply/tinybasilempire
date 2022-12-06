import config
import psycopg2
import psycopg2.extras


def get_db_connection():
    """Database connection."""
    conn = psycopg2.connect(
        host=config.DB_HOST,
        database=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASS,
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
