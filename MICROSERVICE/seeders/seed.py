from utils.log import log
from seeders.suburbs_seeder import seed_suburbs
from seeders.districts_seeder import seed_districts
from seeders.fire_danger_ratings_seeder import retrieve_and_store_bom_data


async def seed(db_cursor):
    log("event", "RUNNING DATABASE SEEDERS")
    seed_districts(db_cursor)
    seed_suburbs(db_cursor)
    return await retrieve_and_store_bom_data(db_cursor, last_issued_at=None)


async def update_if_changed(db_cursor, last_issued_at):
    log("event", "CHECKING FOR UPDATES")
    return await retrieve_and_store_bom_data(db_cursor, last_issued_at=last_issued_at)

