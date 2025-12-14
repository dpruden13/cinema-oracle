import sqlite3


def query_database(statement: str) -> list:
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    # https://docs.python.org/3/library/sqlite3.html#how-to-guides
    res = cur.execute(statement)
    results = res.fetchall()
    con.close()
    return results
