import requests
from ftplib import FTP
from utils.log import log
from bs4 import BeautifulSoup
from time import perf_counter_ns
from datetime import datetime, timedelta


async def bom_scrape(db_cursor, last_issued_at):
    log("info", "Scraping data from BOM website into \"fire_danger_ratings\" table".ljust(96, "."), end="")
    start_time = perf_counter_ns()
    row_count = 0
    url = "http://www.bom.gov.au/wa/forecasts/fire-danger-ratings.shtml"
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
    # Get html content from bom
    request = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(request.content, "html5lib")
    assert soup
    # Get forecast div container
    forecast_div = soup.find("div", class_="forecast")
    # Parse and formate issued at datetime
    issued_at = forecast_div.find("p", class_="date").text
    issued_at = issued_at.replace("Issued at", "").replace("on", "").replace(".", "").replace("WST", "").strip()
    while "  " in issued_at:
        issued_at = issued_at.replace("  ", "")
    issued_at = datetime.strptime(issued_at, '%I:%M %p %A %d %B %Y')
    if last_issued_at:
        if last_issued_at == issued_at:
            exec_time = (perf_counter_ns() - start_time) / 1_000_000
            print(f"ABORTED {exec_time}ms")
            log("info", "No new records to update")
            return issued_at
    # Parse fire danger rating table data
    forecast_tables = forecast_div.find_all("table")
    forecast_rows = forecast_tables[0].find("tbody").find_all("tr")
    current_date = datetime.now().date()
    for row in forecast_rows:
        cells = row.find_all("td")
        district = cells[0].text.strip()
        query = f"SELECT id FROM districts WHERE name = \"{district.upper()}\""
        db_cursor.execute(query)
        result = db_cursor.fetchall()
        district_id = result[0][0]
        for index in range(1, 5):
            split_text = cells[index].text.strip().split(" ")
            rating_name = split_text[0]
            rating_value = split_text[1]
            if len(split_text) == 3:
                rating_name = f"{split_text[0]} {split_text[1]}"
                rating_value = split_text[2]
            rating_date = current_date + timedelta(days=(index - 1))
            # Create and execute query
            query = f"INSERT INTO fire_danger_ratings (district_id, rating_level, rating_name, rating_date, " \
                    f"issued_at, created_at, updated_at) VALUES (\"{district_id}\",{rating_value},\"{rating_name}\"," \
                    f"\"{rating_date}\", \"{issued_at}\", \"{datetime.now()}\", \"{datetime.now()}\")"
            db_cursor.execute(query)
            row_count += 1
    exec_time = (perf_counter_ns() - start_time) / 1_000_000
    print(f"DONE {exec_time}ms")
    log("info", f"INSERTED {row_count} ROWS INTO \"fire_danger_ratings\" TABLE")
    return issued_at


async def bom_ftp(db_cursor, last_issued_at):
    log("info", "Collecting data from BOM FTP for \"fire_danger_ratings\" table".ljust(96, "."), end="")
    start_time = perf_counter_ns()
    ftp = FTP("ftp.bom.gov.au")
    ftp.login()
    lines = []
    remote_path = "anon/gen/fwo/IDW15100.txt"
    ftp.retrlines(f"RETR {remote_path}", lines.append)
    ftp.close()
    data_index = None
    issued_at = None
    row_count = 0
    current_date = datetime.now().date()
    for index, line in enumerate(lines):
        if line == "Code":
            break
        if "Issued at" in line:
            data_index = index + 4
            issued_at = line
            issued_at = issued_at.replace("Issued at", "").replace("on", "").replace(".", "").replace("WST", "").strip()
            while "  " in issued_at:
                issued_at = issued_at.replace("  ", "")
            issued_at = datetime.strptime(issued_at, '%I:%M %p %A %d %B %Y')
            if last_issued_at:
                if last_issued_at == issued_at:
                    exec_time = (perf_counter_ns() - start_time) / 1_000_000
                    print(f"ABORTED {exec_time}ms")
                    log("info", "No new records to update")
                    return issued_at
        if data_index and index >= data_index:
            if line:
                split_line = [split_item for split_item in line.split(" ") if split_item != ""]
                last_index = len(split_line) - 1
                ratings = []
                for _ in range(4):
                    rating_name = "Catastrophic"
                    if split_line[last_index - 1] == "NoR":
                        rating_name = "No Rating"
                    elif split_line[last_index - 1] == "MOD":
                        rating_name = "Moderate"
                    elif split_line[last_index - 1] == "HI":
                        rating_name = "High"
                    elif split_line[last_index - 1] == "EXT":
                        rating_name = "Extreme"
                    ratings.insert(0, [rating_name, split_line[last_index]])
                    last_index -= 2
                last_index += 1
                district_name = " ".join(split_line[:last_index])
                query = f"SELECT id FROM districts WHERE name = \"{district_name.upper()}\""
                db_cursor.execute(query)
                result = db_cursor.fetchall()
                district_id = result[0][0]
                for day_index, day in enumerate(ratings):
                    # Create and execute query
                    rating_date = current_date + timedelta(days=day_index)
                    rating_name = day[0]
                    rating_value = day[1]
                    query = f"INSERT INTO fire_danger_ratings (district_id, rating_level, rating_name, rating_date, " \
                            f"issued_at, created_at, updated_at) VALUES (\"{district_id}\",{rating_value},\"{rating_name}\"," \
                            f"\"{rating_date}\", \"{issued_at}\", \"{datetime.now()}\", \"{datetime.now()}\")"
                    db_cursor.execute(query)
                    row_count += 1
    exec_time = (perf_counter_ns() - start_time) / 1_000_000
    print(f"DONE {exec_time}ms")
    log("info", f"INSERTED {row_count} ROWS INTO \"fire_danger_ratings\" TABLE")
    return issued_at


async def retrieve_and_store_bom_data(db_cursor, last_issued_at=None):
    use_fallback = False
    new_issued_at = None
    try:
        new_issued_at = await bom_scrape(db_cursor, last_issued_at)
    except Exception as e:
        log("error", str(e))
        use_fallback = True
    if not use_fallback:
        return new_issued_at
    log("error", "Failed to scrape data from BOM website, using FTP fallback retrieval.")
    try:
        new_issued_at = await bom_ftp(db_cursor, last_issued_at)
    except Exception as e:
        log('error', str(e))
        log("error", "Failed to retrieve data from BOM FTP server")
    return new_issued_at

