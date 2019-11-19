# def test_get_databases(client):
#     res = client.post("postgres/databases", data=dict(
#         user="postgres",
#         password="",
#         host="localhost",
#         port=5432
#     ), headers={"Content-Type": "application/json"})
#     assert res.status_code == 200
#
#
# def test_get_snowflake_databases(client):
#     res = client.post("snowflake/databases", data=dict(
#         user="dhan",
#         password="4M9YZXECHKpQFj6nbpHqTYNCAMb92dnWoqzBvEME",
#         account="hj72458.us-east-1"
#     ), headers={"Content-Type": "application/json"})
#     assert res.status_code == 200
#
#
