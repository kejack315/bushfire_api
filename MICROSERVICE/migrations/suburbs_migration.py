from utils.log import log
from time import perf_counter_ns


def create_suburbs_table(db_cursor):
    # Drop and create empty suburbs table
    log("info", "Creating \"suburbs\" table".ljust(48, "."), end="")
    start_time = perf_counter_ns()
    db_cursor.execute("DROP TABLE IF EXISTS suburbs")
    db_cursor.execute(""" CREATE TABLE suburbs (
                id INTEGER PRIMARY KEY, 
                name VARCHAR(255), 
                postal_code VARCHAR(16),
                latitude DECIMAL(9, 6),
                longitude DECIMAL(9, 6),
                created_at TIMESTAMP,
                updated_at TIMESTAMP
            ); """)
    exec_time = (perf_counter_ns() - start_time) / 1_000_000
    print(f"DONE {exec_time}ms")
