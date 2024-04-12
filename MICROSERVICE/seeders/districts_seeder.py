from utils.log import log
from datetime import datetime
from time import perf_counter_ns


def seed_districts(db_cursor):
    # District seed data
    log("info", "Seeding \"districts\" table".ljust(64, "."), end="")
    start_time = perf_counter_ns()
    row_count = 0
    district_names = [
                "North Kimberley",
                "Derby Coast",
                "Broome Coast",
                "Kimberley Inland",
                "Central Pilbara",
                "Hedland",
                "Burrup",
                "Ashburton Inland",
                "Ashburton Coast",
                "Exmouth Gulf Coast",
                "North Interior",
                "Gascoyne Coast",
                "Gascoyne Inland",
                "Yalgar",
                "North Goldfields",
                "South Goldfields",
                "West Interior",
                "Central Interior",
                "South Interior",
                "Eucla",
                "Midwest Coast",
                "Midwest Inland",
                "Lesueur",
                "Yarra Yarra",
                "Swan Coastal North",
                "Swan Inland North",
                "Swan Coastal South",
                "Swan Inland South",
                "Geographe",
                "Capes",
                "Brockman",
                "Blackwood",
                "Southern Forests",
                "Mortlock",
                "Karroun",
                "Avon",
                "Lockwood",
                "Arthur",
                "Roe",
                "Lakes",
                "Stirling North",
                "Stirling West",
                "Stirling Coast",
                "Fitzgerald Coast",
                "Fitzgerald Inland",
                "Esperance Coast",
                "Esperance Inland",
            ]
    for district in district_names:
        db_cursor.execute(f"""INSERT INTO districts (name, created_at, updated_at) 
                    VALUES (\"{district.upper()}\", \"{datetime.now()}\", \"{datetime.now()}\");""")
        row_count += 1
    exec_time = (perf_counter_ns() - start_time) / 1_000_000
    print(f"DONE {exec_time}ms")
    log("info", f"INSERTED {row_count} ROWS INTO \"districts\" TABLE")
