import json
import logging
from sqlalchemy import create_engine, text
from app.lib.helpers import resultproxy_to_dict_stream

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


class SnowflakeInspector:
    def __init__(self, *, user, password, account, database=""):
        self.database = database
        self.engine = create_engine(
            f"snowflake://{user}:{password}@{account}/{database}"
        )
        self.connection = self.engine.connect()

    def __resultproxy_to_dict_stream(self, sql_alchemy_rowset):
        for rowproxy in sql_alchemy_rowset:
            d = {}
            # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
            for column, value in rowproxy.items():
                # build up the dictionary
                d = {**d, **{column: value}}
            yield json.dumps(d, default=str) + "\n"

    def __make_request(self, query):
        resultproxy = self.connection.execute(query)
        return resultproxy_to_dict_stream(resultproxy)

    def list_databases(self):
        for row in self.__make_request("show databases"):
            yield {"database_name": row["name"], "created_at": row["created_on"]}

    def list_tables(self):
        # TODO, investigate proper sanitization. https://stackoverflow.com/questions/43877210/how-to-remove-the-quotes-from-a-string-for-sql-query-in-python
        for row in self.__make_request(
            text(f"show tables in database {self.database}")
        ):
            yield {
                "table_name": row["name"],
                "schema_name": row["schema_name"],
                "created_at": row["created_on"],
            }

    def list_columns(self, *, schema, table):
        for row in self.__make_request(
            text(f"show columns in table {self.database}.{schema}.{table}")
        ):
            yield {
                "column_name": row["column_name"],
                "table_name": row["table_name"],
                "schema_name": row["schema_name"],
                "data_type": json.loads(row["data_type"])["type"],
            }
        return

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
