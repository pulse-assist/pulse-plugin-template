"""Тесты плагина без Пульса: API Пульса подменяется. Запуск из папки backend: python -m pytest"""

import os

os.environ.setdefault("PULSE_PLUGIN_SETTINGS", '{"greeting": "Здравствуйте", "threshold": 2}')

from fastapi.testclient import TestClient  # noqa: E402

from example_plugin import app as module  # noqa: E402


class FakeApi:
    def __init__(self, totals):
        self.totals = totals
        self.posted = []

    def get(self, path, **params):
        return {"total": self.totals[params["type"]], "items": []}

    def post(self, path, body=None):
        self.posted.append(body)
        return {"id": "sig1", **body}


def make_client(monkeypatch, totals):
    fake = FakeApi(totals)
    monkeypatch.setitem(module.plugin.__dict__, "api", fake)     # plugin.api — cached_property: подменяем значение
    return TestClient(module.app), fake


def test_health_and_summary(monkeypatch):
    http, _ = make_client(monkeypatch, {"task": 3, "signal": 5, "knowledge": 1})
    assert http.get("/health").json()["ok"] is True
    assert http.get("/summary").json() == {"greeting": "Здравствуйте", "counts": {"task": 3, "signal": 5, "knowledge": 1}}
    assert http.post("/commands/summary", json={}).json() == {"task": 3, "signal": 5, "knowledge": 1}


def test_check_creates_signal_over_threshold(monkeypatch):
    http, fake = make_client(monkeypatch, {"task": 3, "signal": 0, "knowledge": 0})
    assert http.post("/commands/check", json={}).json() == {"open_tasks": 3, "threshold": 2, "signal": "sig1"}
    assert fake.posted[0]["type"] == "signal" and fake.posted[0]["priority"] == 75
    assert http.post("/commands/check", json={"threshold": 5}).json()["signal"] is None
    assert http.post("/commands/check", json={"threshold": "x"}).status_code == 400
