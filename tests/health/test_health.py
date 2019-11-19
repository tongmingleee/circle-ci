def test_health(client):
    res = client.get("/health", follow_redirects=True)
    assert res.status_code == 200
