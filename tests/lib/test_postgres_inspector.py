def test_list_databases(postgres_inspector):
    res = list(postgres_inspector.list_databases())

    # these are default databases in PostgresSQL
    expected = [
        {"database_name": "postgres"},
        {"database_name": "test"},
        {"database_name": "template1"},
        {"database_name": "template0"},
    ]

    assert expected == res


def test_list_tables(postgres_inspector):
    res = list(postgres_inspector.list_tables())
    expected = [{"schema_name": "public", "table_name": "person"}]

    assert expected == res


def test_list_columns(postgres_inspector):
    res = list(postgres_inspector.list_columns(schema="public", table="person"))
    expected = [
        {"column_name": "id", "data_type": "integer"},
        {"column_name": "name", "data_type": "character varying"},
    ]

    assert expected == res


def test_get_fresh_data(postgres_inspector):
    res = list(
        postgres_inspector.get_fresh_data(schema="public", table="person", limit=100)
    )

    print(res)
    expected = [{"id": 1, "name": "King"}, {"id": 2, "name": "Jon"}]
    assert expected == res
