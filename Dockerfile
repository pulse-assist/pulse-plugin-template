# Плагин контейнером — для runtime.kind = "docker" (и для плагинов не на Python: тогда свой образ целиком).
# Перед сборкой Пульс кладёт пакет pulse_plugin в контекст сборки: .pulse_plugin_sdk/
# Локально: cp -r ../pulse/plugin_sdk .pulse_plugin_sdk && docker build -t my-plugin .
FROM python:3.12-slim
WORKDIR /plugin
COPY .pulse_plugin_sdk /tmp/pulse_plugin
COPY backend/requirements.txt backend/requirements.txt
RUN pip install --no-cache-dir /tmp/pulse_plugin && pip install --no-cache-dir -r backend/requirements.txt
COPY . .
WORKDIR /plugin/backend
# порт задаёт Пульс (PULSE_PLUGIN_PORT); данные — /plugin/data, папка в «Файлах» — /plugin/files
ENV PULSE_PLUGIN_PORT=8080
CMD ["sh", "-c", "exec uvicorn example_plugin.app:app --host 0.0.0.0 --port ${PULSE_PLUGIN_PORT}"]
