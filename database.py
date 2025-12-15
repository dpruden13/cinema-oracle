import sqlite3
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename='cinema_oracle.log', level=logging.INFO)


def query_database(statement: str) -> list:
    logger.info(f'Executing SQL statement: {statement}')
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    # https://docs.python.org/3/library/sqlite3.html#how-to-guides
    res = cur.execute(statement)
    results = res.fetchall()
    con.close()
    return results
