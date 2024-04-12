import uvicorn
import sqlite3
import asyncio
from utils.log import log
from time import perf_counter_ns
from utils.logo import print_logo
from fastapi import Request, FastAPI
from migrations.migrate import migrate
from contextlib import asynccontextmanager
from seeders.seed import seed, update_if_changed
from controllers.fire_danger_rating_controller import handle_fire_danger_rating_request, \
    get_all_current_fire_danger_ratings

service_start_time: int = 0
req_cnt: int = 0
sync_rate: int = 60
is_syncing: bool = False
first_run: bool = True


async def request_rate() -> float:
    global service_start_time
    elapsed_time_s = (perf_counter_ns() - service_start_time) / 1_000_000_000
    return req_cnt / elapsed_time_s


async def sync_data() -> None:
    global is_syncing, sync_rate, first_run
    last_issued_at = None
    while True:
        start_time = perf_counter_ns()
        connection = sqlite3.connect("bushfire_warnings.db")
        db_cursor = connection.cursor()
        log("EVENT", "RUNNING DATA SYNC")
        is_syncing = True
        if first_run:
            migrate(db_cursor)
            new_issued_at = await seed(db_cursor)
            first_run = False
        else:
            new_issued_at = await update_if_changed(db_cursor, last_issued_at)
        last_issued_at = new_issued_at
        connection.commit()
        connection.close()
        exec_time = (perf_counter_ns() - start_time) / 1_000_000
        log("EVENT", f"DATA SYNC COMPLETE IN {exec_time}ms")
        is_syncing = False
        await asyncio.sleep(sync_rate)


@asynccontextmanager
async def lifespan(app_: FastAPI):
    global service_start_time
    service_start_time = perf_counter_ns()
    print_logo()
    asyncio.create_task(sync_data())
    yield
    log('event', "TERMINATING MICROSERVICE")


app = FastAPI(lifespan=lifespan)


@app.post("/fire-danger-ratings")
async def fire_danger_ratings(req: Request):
    start_time = perf_counter_ns()
    global is_syncing, req_cnt
    req_cnt += 1
    log("debug", f"Request rate: {await request_rate()}")
    while is_syncing:
        log("warning", "503 DATABASE SYNC IN PROGRESS")
        pass
    try:
        req_body = await req.body()
        res = await handle_fire_danger_rating_request(req_body)
        exec_time = (perf_counter_ns() - start_time) / 1_000_000
        log("post", f"200 OK - Process time: {exec_time}ms")
        return res
    except Exception as e:
        exec_time = (perf_counter_ns() - start_time) / 1_000_000
        log("error", f"ERROR {e} - Process time: {exec_time}ms")
        return {"status": 500, "error": "an unknown error occurred"}


@app.get("/fire-danger-ratings/all")
async def all_fire_danger_ratings(req: Request):
    start_time = perf_counter_ns()
    global is_syncing, req_cnt
    req_cnt += 1
    log("debug", f"Request rate: {await request_rate()}")
    while is_syncing:
        log("warning", "503 DATABASE SYNC IN PROGRESS")
        pass
    try:
        res = await get_all_current_fire_danger_ratings()
        exec_time = (perf_counter_ns() - start_time) / 1_000_000
        log("post", f"200 OK - Process time: {exec_time}ms")
        return res
    except Exception as e:
        exec_time = (perf_counter_ns() - start_time) / 1_000_000
        log("error", f"ERROR {e} - Process time: {exec_time}ms")
        return {"status": 500, "error": "an unknown error occurred"}


@app.get("/suburb-list")
async def suburb_list(req: Request):
    start_time = perf_counter_ns()
    global is_syncing, req_cnt
    req_cnt += 1
    log("debug", f"Request rate: {await request_rate()}")
    while is_syncing:
        log("warning", "503 DATABASE SYNC IN PROGRESS")
        pass
    try:
        connection = sqlite3.connect("bushfire_warnings.db")
        db_cursor = connection.cursor()        
        db_cursor.execute("SELECT id, name FROM suburbs")
        all_suburbs = db_cursor.fetchall()
        res_obj = {}
        if all_suburbs:
            for sub in all_suburbs:
                res_obj[sub[0]] = sub[1]
        connection.commit()
        connection.close()
        exec_time = (perf_counter_ns() - start_time) / 1_000_000
        log("post", f"200 OK - Process time: {exec_time}ms")
        return {"status": 200, "suburbs": res_obj}
    except Exception as e:
        exec_time = (perf_counter_ns() - start_time) / 1_000_000
        log("error", f"ERROR {e} - Process time: {exec_time}ms")
        return {"status": 500, "error": "an unknown error occurred"}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)

