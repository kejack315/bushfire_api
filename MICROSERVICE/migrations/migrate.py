from utils.log import log
from migrations.suburbs_migration import create_suburbs_table
from migrations.districts_migration import create_districts_table
from migrations.fire_danger_ratings_migration import create_fire_danger_ratings_table


def migrate(db_cursor):
    log("event", "RUNNING MIGRATIONS")
    create_districts_table(db_cursor)
    create_suburbs_table(db_cursor)
    create_fire_danger_ratings_table(db_cursor)
