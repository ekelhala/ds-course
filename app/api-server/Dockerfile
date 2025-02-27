FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 80
ENV RABBITMQ_USERNAME guest
ENV RABBITMQ_PASSWORD guest
ENV RABBITMQ_BROKER 127.0.0.1
ENV RABBITMQ_PORT 5672
CMD ["fastapi", "run", "main.py", "--port", "80"]