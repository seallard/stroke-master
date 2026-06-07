def test_health_response(monkeypatch):
    from fastapi.testclient import TestClient

    import app.main as main

    # Stub the DB pool lifecycle so the health check needs no Postgres.
    async def _noop():
        return None

    monkeypatch.setattr(main, "open_pool", _noop)
    monkeypatch.setattr(main, "close_pool", _noop)

    with TestClient(main.app) as client:
        resp = client.get("/health")
        assert resp.status_code == 200
        assert resp.json() == {"status": "ok"}
