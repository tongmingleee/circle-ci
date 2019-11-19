from sqlalchemy import create_engine, text
from app.lib.helpers import resultproxy_to_dict_stream


class PostgresInspector:
    def __init__(self, *, user, password, host, port, database=""):
        self.engine = create_engine(
            f"postgres://{user}:{password}@{host}:{port}/{database}"
        )
        self.connection = self.engine.connect()

    def __make_request(self, query):
        resultproxy = self.connection.execute(query)
        return resultproxy_to_dict_stream(resultproxy)

    def list_databases(self):
        for row in self.__make_request(
            "SELECT datname as database_name FROM pg_database;"
        ):
            yield {"database_name": row["database_name"]}

    def list_tables(self):
        # TODO, investigate proper sanitization. https://stackoverflow.com/questions/43877210/how-to-remove-the-quotes-from-a-string-for-sql-query-in-python
        for row in self.__make_request(
            text(
                """
            SELECT
                schemaname as schema_name,
                tablename as table_name
            FROM
                pg_catalog.pg_tables
            WHERE
                schemaname != 'pg_catalog'
            AND schemaname != 'information_schema';"""
            )
        ):

            yield {"schema_name": row["schema_name"], "table_name": row["table_name"]}

    def list_columns(self, *, schema, table):
        for row in self.__make_request(
            text(
                f"""
            SELECT
            column_name as column_name,
            data_type as data_type
            FROM information_schema.columns
            WHERE table_schema = '{schema}'
            AND table_name   = '{table}';"""
            )
        ):
            yield {"column_name": row["column_name"], "data_type": row["data_type"]}

    def get_fresh_data(
        self,
        *,
        schema,
        table,
        limit,
        fields=None,
        updated_since=None,
        updated_at_field=None,
    ):
        projection = " * "
        source = f"{schema}.{table}"
        where_clause = ""

        if fields:
            projection = (", ").join(fields)

        if updated_at_field and updated_since:
            where_clause = f" where {updated_at_field} :: timestamp > '{updated_since}' :: timestamp "

        return self.__make_request(
            f"""
        select
            {projection}
        from {source}
        {where_clause}
        limit {limit}"""
        )
