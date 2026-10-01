from psycopg import connect
from psycopg.rows import dict_row
import config

def get_connection():
    return connect(
        host = config.hostname,
        dbname = config.database,
        password = config.pwd,
        user = config.username,
        port = config.port_id,
        row_factory = dict_row
    )

def get_db():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            yield cursor