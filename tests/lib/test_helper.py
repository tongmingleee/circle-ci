from app.lib.helpers import resultproxy_to_dict_stream, to_jsonl_stream


def mock_result_proxy():
    sql_alchemy_rowset = [
        {"database_name": "DEMO_DB", "created_at": "2019-10-04 13:31:21.568000-07:00"},
        {
            "database_name": "SNOWFLAKE_SAMPLE_DATA",
            "created_at": "2019-10-04 13:31:22.500000-07:00",
        },
    ]
    return sql_alchemy_rowset


def test_resultproxy_to_dict_stream():
    # test with empty object
    res = list(resultproxy_to_dict_stream({}))
    assert res == []

    # test with valid object
    mock = mock_result_proxy()
    res = list(resultproxy_to_dict_stream(mock))
    assert len(res) == 2
    assert res == mock


def test_to_jsonl_stream():
    # test with empty object
    res = list(to_jsonl_stream({}))
    assert res == []

    # test with valid object
    res = list(to_jsonl_stream(mock_result_proxy()))
    expected = [
        '{"database_name": "DEMO_DB", "created_at": "2019-10-04 13:31:21.568000-07:00"}\n',
        '{"database_name": "SNOWFLAKE_SAMPLE_DATA", "created_at": "2019-10-04 13:31:22.500000-07:00"}\n',
    ]
    assert res == expected
