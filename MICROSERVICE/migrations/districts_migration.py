from utils.log import log
from time import perf_counter_ns


def create_districts_table(db_cursor):
    # Drop and create empty districts table
    log("info", "Creating \"districts\" table".ljust(64, "."), end="")
    start_time = perf_counter_ns()
    db_cursor.execute("DROP TABLE IF EXISTS districts")
    db_cursor.execute(""" CREATE TABLE districts (
                id INTEGER PRIMARY KEY, 
                name VARCHAR(255),
                created_at TIMESTAMP,
                updated_at TIMESTAMP
            ); """)
    exec_time = (perf_counter_ns() - start_time) / 1_000_000
    print(f"DONE {exec_time}ms")
