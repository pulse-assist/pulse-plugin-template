"""Тесты плагина без Пульса: API Пульса подменяется. Запуск из папки backend: python -m pytest"""

import os

os.environ.setdefault("PULSE_PLUGIN_SETTINGS", '{"greeting": "Здравствуйте", "threshold": 2}')

from fastapi.testclient import TestClient  # noqa: E402
from pulse_plugin.testing import fake_api  # noqa: E402

from example_plugin import app as module  # noqa: E402


def make_client(monkeypatch, totals):
    """API Пульса подменён: на GET /api/cards — счётчик по типу, сигналы запоминаются (api.signals)."""
    api = fake_api(module.plugin, monkeypatch)
    api.on("GET", "/api/cards", lambda params, body: {"total": totals[params["type"]], "items": []})
    return TestClient(module.app), api


def test_health_and_summary(monkeypatch):
    http, _ = make_client(monkeypatch, {"task": 3, "signal": 5, "knowledge": 1})
    assert http.get("/health").json()["ok"] is True
    assert http.get("/summary").json() == {"greeting": "Здравствуйте", "counts": {"task": 3, "signal": 5, "knowledge": 1}}
    assert http.post("/commands/summary", json={}).json() == {"task": 3, "signal": 5, "knowledge": 1}


def test_check_creates_signal_over_threshold(monkeypatch):
    http, fake = make_client(monkeypatch, {"task": 3, "signal": 0, "knowledge": 0})
    assert http.post("/commands/check", json={}).json() == {"open_tasks": 3, "threshold": 2, "signal": "signal-1"}
    assert fake.signals[0]["priority"] == 75
    assert http.post("/commands/check", json={"threshold": 5}).json()["signal"] is None
    assert http.post("/commands/check", json={"threshold": "x"}).status_code == 400
