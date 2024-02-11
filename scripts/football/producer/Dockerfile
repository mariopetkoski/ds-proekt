FROM python:3.11-slim
WORKDIR /app
COPY football_producer.py .
RUN chmod +x football_producer.py
COPY models.py .
COPY data_generator.py .
RUN pip install --no-cache-dir confluent-kafka
ENTRYPOINT [ "python", "football_producer.py" ]