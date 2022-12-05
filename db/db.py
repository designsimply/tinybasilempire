import os
import psycopg2
import psycopg2.extras

# database connection
def get_db_connection():
    conn = psycopg2.connect(host='localhost',
        database='stuffdb',
        # TDDO move these variables to config. config.DB_USERNAME 
        # any os.environ should be in config
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD'])
    return conn

# do all the sql!
def query_db(sql, params=None):
    with get_db_connection() as conn:
        conn.autocommit=True
        with conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) as cur:
            cur.execute(sql, params)
            try:
                return list(cur.fetchall())
            except psycopg2.ProgrammingError:
                return []

