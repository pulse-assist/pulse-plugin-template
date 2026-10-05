"""Серверная часть плагина: команды для агентов, свой API для страницы, сигнал в ленту.

Пульс запускает этот модуль как `uvicorn example_plugin.app:app` и передаёт окружение (см. AGENTS.md):
plugin.settings, plugin.secret(...), plugin.api (токен плагина), plugin.data_dir, plugin.files_dir.
"""

from pulse_plugin import CommandError, Plugin

plugin = Plugin()
app = plugin.app            # /health и /commands/... уже есть


def count_cards() -> dict:
    """Сколько карточек каждого типа — через API Пульса с правами плагина (cards:read)."""
    return {kind: plugin.api.get("/api/cards", type=kind, limit=1)["total"] for kind in ("task", "signal", "knowledge")}


@plugin.command("summary", "Сколько карточек каждого типа")
def summary_command(args: dict) -> dict:
    return count_cards()


@plugin.command("check", "Открытых задач больше порога — сигнал в ленту")
def check_command(args: dict) -> dict:
    try:
        threshold = int(args.get("threshold") or plugin.setting("threshold", 10))
    except ValueError as exc:
        raise CommandError("--threshold — целое число") from exc
    open_tasks = plugin.api.get("/api/cards", type="task", archived="false", limit=1)["total"]
    if open_tasks <= threshold:
        return {"open_tasks": open_tasks, "threshold": threshold, "signal": None}
    signal = plugin.signal(f"Открытых задач: {open_tasks} — больше порога {threshold}",
                           body="Пора разобрать доску задач.", priority=75, tags=["пример-плагина"])
    return {"open_tasks": open_tasks, "threshold": threshold, "signal": signal["id"]}


@app.get("/summary")
def summary_api() -> dict:
    """Для страницы плагина: pulse.plugin("/summary")."""
    return {"greeting": plugin.setting("greeting", "Привет"), "counts": count_cards()}
