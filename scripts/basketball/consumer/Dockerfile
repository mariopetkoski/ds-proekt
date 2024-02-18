FROM python:3.11-slim
WORKDIR /app
COPY basketball_consumer.py .
COPY basketball.ndjson .
RUN chmod +x basketball_consumer.py
RUN pip install --no-cache-dir opensearch-py confluent-kafka
ENTRYPOINT [ "python", "basketball_consumer.py" ]