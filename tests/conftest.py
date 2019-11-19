import pytest
import testing.postgresql
from sqlalchemy import create_engine

from app import create_app
from app.lib.postgres import PostgresInspector

# TODO: add some doc/explaination
@pytest.fixture
def client():
    client = create_app().test_client()
    return client


# TODO: make global? or static or from config file
user = "postgres"
password = ""
host = "localhost"
port = 5432


def handler(postgres):
    engine = create_engine(postgres.url(database="postgres"))
    conn = engine.connect()

    # create some dummy data
    conn.execute("DROP TABLE IF EXISTS person")
    conn.execute("CREATE TABLE IF NOT EXISTS person(id int, name varchar(256))")
    conn.execute("INSERT INTO person VALUES(1, 'King'), (2, 'Jon')")

    # close connection
    conn.close()


@pytest.fixture(scope="module")
def postgres():
    postgres = testing.postgresql.PostgresqlFactory(
        name=user, port=port, cache_initialized_db=True, on_initialized=handler
    )
    yield postgres

    # clear cached database at end of tests
    postgres.clear_cache()


@pytest.fixture(scope="module")
def postgres_inspector(postgres):
    postgres_inspector = PostgresInspector(user=user, password="", host=host, port=port)
    return postgres_inspector


# TODO: create snowflake fixture
