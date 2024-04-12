from utils.log import log
from time import perf_counter_ns


def create_fire_danger_ratings_table(db_cursor):
    # Drop and create empty fire ratings table
    log("info", "Creating \"fire_danger_ratings\" table".ljust(64, "."), end="")
    start_time = perf_counter_ns()
    db_cursor.execute("DROP TABLE IF EXISTS fire_danger_ratings")
    db_cursor.execute(""" CREATE TABLE fire_danger_ratings (
                id INTEGER PRIMARY KEY, 
                district_id INTEGER,
                rating_level INTEGER,
                rating_name VARCHAR(128),
                rating_date TIMESTAMP,
                issued_at TIMESTAMP,
                created_at TIMESTAMP,
                updated_at TIMESTAMP
            ); """)
    exec_time = (perf_counter_ns() - start_time) / 1_000_000
    print(f"DONE {exec_time}ms")
