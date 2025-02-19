import os
import pika

class AMQPClient():

    def __init__(self):
        self._connection: pika.BlockingConnection = None
        self._channel: pika.channel.Channel = None
        self._queue_name = "work-queue"

    def connect(self):
        connection_credentials = pika.PlainCredentials(username=os.getenv("RABBITMQ_USERNAME"),
                                                        password=os.getenv("RABBITMQ_PASSWORD"))
        connection_params = pika.ConnectionParameters(
                                                        host=os.getenv("RABBITMQ_BROKER"),
                                                        port=os.getenv("RABBITMQ_PORT"),
                                                        credentials=connection_credentials)
        self._connection = pika.BlockingConnection(parameters=connection_params)
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue=self._queue_name)

    def send(self, message):
        self._channel.basic_publish(exchange="",
                                    routing_key=self._queue_name,
                                    body=message)
    
    def close(self):
        self._connection.close()
