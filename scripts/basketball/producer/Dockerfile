FROM python:3.11-slim
WORKDIR /app
COPY basketball_producer.py .
RUN chmod +x basketball_producer.py
COPY models.py .
COPY data_generator.py .
RUN pip install --no-cache-dir confluent-kafka
ENTRYPOINT [ "python", "basketball_producer.py" ]