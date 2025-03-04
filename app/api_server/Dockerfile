FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn
RUN mkdir api_server
WORKDIR /app/api_server
COPY . .
ENV RABBITMQ_USERNAME guest
ENV RABBITMQ_PASSWORD guest
ENV RABBITMQ_BROKER 127.0.0.1
ENV RABBITMQ_PORT 5672
ENV MONGODB_URI mongodb://127.0.0.1:27017
WORKDIR /app
CMD ["gunicorn", "-b", "0.0.0.0:80", "api_server.app:app"]