FROM python:3.11-slim
WORKDIR /app
COPY football_consumer.py .
COPY football.ndjson .
RUN chmod +x football_consumer.py
RUN pip install --no-cache-dir opensearch-py confluent-kafka
ENTRYPOINT [ "python", "football_consumer.py" ]