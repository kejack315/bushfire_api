import os
import json
from utils.log import log
from datetime import datetime
from time import perf_counter_ns


def seed_suburbs(db_cursor):
    log("info", "Seeding \"suburbs\" table".ljust(64, "."), end="")
    start_time = perf_counter_ns()
    row_count = 0
    file_path = os.path.join(os.getcwd(), "data", "seed_data", "australian_postcodes.json")
    with open(file_path, "r") as auspost_file:
        auspost_json = json.loads(auspost_file.read())
    for entry in auspost_json:
        if entry["state"] == "WA":
            query = f"INSERT INTO suburbs (name, postal_code, latitude, longitude, created_at, updated_at) " \
                    f"VALUES (\"{entry['locality']}\", \"{entry['postcode']}\", \"{entry['lat']}\", \"{entry['long']}\", " \
                    f"\"{datetime.now()}\", \"{datetime.now()}\")"
            db_cursor.execute(query)
            row_count += 1
    exec_time = (perf_counter_ns() - start_time) / 1_000_000
    print(f"DONE {exec_time}ms")
    log("info", f"INSERTED {row_count} ROWS INTO \"suburbs\" TABLE")
