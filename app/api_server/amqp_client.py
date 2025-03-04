import json
import uuid
import os
import pika
from dotenv import load_dotenv

class AMQPClient():

    def __init__(self):
        self._connection: pika.BlockingConnection = None
        self._channel: pika.channel.Channel = None
        self._queue_name = "work-queue"
        self._correlation_id = None
        self._reply_queue = None
        self._response = None

    def _on_message(self, cd, method, props, body):
        if self._correlation_id == props.correlation_id:
            self._response = body

    def connect(self):
        load_dotenv()
        connection_credentials = pika.PlainCredentials(username=os.getenv("RABBITMQ_USERNAME"),
                                                        password=os.getenv("RABBITMQ_PASSWORD"))
        connection_params = pika.ConnectionParameters(
                                                        host=os.getenv("RABBITMQ_BROKER"),
                                                        port=os.getenv("RABBITMQ_PORT"),
                                                        credentials=connection_credentials)
        self._connection = pika.BlockingConnection(parameters=connection_params)
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue=self._queue_name)
        self._reply_queue = self._channel.queue_declare(queue='', exclusive=True).method.queue
        self._channel.basic_consume(
            queue=self._reply_queue,
            on_message_callback=self._on_message,
            auto_ack=True
        )

    def send(self, message):
        self._correlation_id = str(uuid.uuid4())
        self._response = None
        self._channel.basic_publish(exchange="",
                                    routing_key=self._queue_name,
                                    properties=pika.BasicProperties(
                                        reply_to=self._reply_queue,
                                        correlation_id=self._correlation_id
                                    ),
                                    body=message)
        while self._response is None:
            self._connection.process_data_events()
        response_decoded = self._response.decode("utf-8")
        return json.loads(response_decoded)
    
    def close(self):
        self._channel.close()
        self._connection.close()
