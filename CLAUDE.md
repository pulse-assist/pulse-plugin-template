# Плагин «Пульса» — инструкция для Claude Code

Полная инструкция по разработке — [AGENTS.md](AGENTS.md), контракт платформы — CONTRACT.md пакета
pulse-plugin (pulse-assist/pulse-plugin-sdk); прочитай оба перед работой. Главное:

- Это плагин для «Пульса»: манифест `pulse-plugin.json`, сервер на `pulse_plugin` (`backend/`), страницы во
  фрейме с мостом `window.pulse` (`ui/`), команды агентов (`commands.json`), скиллы и агенты, `INSTALL.md`.
- Тексты для владельца и агентов — по-русски.
- Права — минимально нужные; всё вне `permissions` Пульс отклоняет.
- Страницы не ходят в API Пульса напрямую — только через `pulse.plugin`, `pulse.api`, `pulse.command`.
- После изменений: `pulse-plugin check` и `cd backend && python -m pytest`; `commands.json` и `INSTALL.md`
  соответствуют коду. Живая проверка — `pulse-plugin dev --pulse … --token …`.
- Релиз — поднять `version` в манифесте и поставить тег `v<версия>`: CI соберёт релиз; в каталог —
  `pulse-plugin publish` и MR. Новые права — только осознанно, с объяснением в README и `changes`.
