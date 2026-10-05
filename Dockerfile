# Тот же плагин как контейнер — для runtime.kind = "docker" (следующий этап Пульса) и плагинов на других языках.
# Python-плагину с kind = "python" этот файл не нужен: Пульс запускает его в своём окружении или в venv.
FROM python:3.12-slim
WORKDIR /plugin
COPY backend/requirements.txt backend/requirements.txt
RUN pip install --no-cache-dir "pulse-plugin @ git+https://github.com/pulse-assist/pulse.git#subdirectory=plugin_sdk" \
    && pip install --no-cache-dir -r backend/requirements.txt
COPY . .
WORKDIR /plugin/backend
ENV PULSE_PLUGIN_PORT=8080
CMD ["sh", "-c", "uvicorn example_plugin.app:app --host 0.0.0.0 --port ${PULSE_PLUGIN_PORT}"]
