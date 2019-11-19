import json

from sqlalchemy.engine import ResultProxy


def resultproxy_to_dict_stream(sql_alchemy_rowset=ResultProxy):
    for rowproxy in sql_alchemy_rowset:
        d = {}
        # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
        for column, value in rowproxy.items():
            # build up the dictionary
            d = {**d, **{column: value}}
        yield d


def to_jsonl_stream(iterable):
    for item in iterable:
        yield json.dumps(item, default=str) + "\n"
