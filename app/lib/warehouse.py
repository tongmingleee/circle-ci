from app.lib.postgres import PostgresInspector
from app.lib.snowflake import SnowflakeInspector

Handlers = {"snowflake": SnowflakeInspector, "postgres": PostgresInspector}


def get_warehouse_handler(type, credentials):
    return Handlers[type](**credentials)
