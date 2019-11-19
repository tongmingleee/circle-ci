from flask import Blueprint, request, Response

from app.lib.helpers import to_jsonl_stream
from app.lib.warehouse import get_warehouse_handler

bp = Blueprint("routes", __name__)


@bp.route("/<string:data_source_type>/databases", methods=["POST"])
def get_databases(data_source_type):
    warehouse_handler = get_warehouse_handler(data_source_type, request.json)

    return Response(to_jsonl_stream(warehouse_handler.list_databases()))


@bp.route(
    "/<string:data_source_type>/databases/<string:database>/schemas", methods=["POST"]
)
def get_database_tables(data_source_type, database):
    auth = request.json
    auth["database"] = database
    warehouse_handler = get_warehouse_handler(data_source_type, auth)

    return Response(to_jsonl_stream(warehouse_handler.list_tables()))


@bp.route(
    "/<string:data_source_type>/databases/<string:database>/schemas/<string:schema>/tables/<string:table>/columns",
    methods=["POST"],
)
def get_table_columns(data_source_type, database, schema, table):
    auth = request.json
    auth["database"] = database
    warehouse_handler = get_warehouse_handler(data_source_type, auth)

    return Response(
        to_jsonl_stream(warehouse_handler.list_columns(schema=schema, table=table))
    )


@bp.route(
    "/<string:data_source_type>/databases/<string:database>/schemas/<string:schema>/tables/<string:table>",
    methods=["POST"],
)
def get_data(data_source_type, database, schema, table):
    auth = request.json
    auth["database"] = database
    limit = request.args.get("limit") if request.args.get("limit") else "1000"
    warehouse_handler = get_warehouse_handler(data_source_type, auth)

    fields_str = request.args.get("fields")
    fields = fields_str.split(",") if fields_str is not None else None

    updated_at_field = request.args.get("updated_at_field")
    updated_since = request.args.get("updated_since")

    return Response(
        to_jsonl_stream(
            warehouse_handler.get_fresh_data(
                schema=schema,
                table=table,
                limit=limit,
                fields=fields,
                updated_at_field=updated_at_field,
                updated_since=updated_since,
            )
        )
    )
