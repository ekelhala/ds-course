FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV RABBITMQ_USERNAME guest
ENV RABBITMQ_PASSWORD guest
ENV RABBITMQ_BROKER 127.0.0.1
ENV RABBITMQ_PORT 5672
# expose metrics port
EXPOSE 9000
CMD ["python", "main.py"]
