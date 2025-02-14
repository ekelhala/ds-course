import os
import pika

class AMQPClient():

    def __init__(self):
        self.connection = None

    def connect(self):
        connection_credentials = pika.PlainCredentials(username=os.getenv("RABBITMQ_USERNAME"),
                                                        password=os.getenv("RABBITMQ_PASSWORD"))
        connection_params = pika.ConnectionParameters(
                                                        host=os.getenv("RABBITMQ_BROKER"),
                                                        port=os.getenv("RABBITMQ_PORT"),
                                                        credentials=connection_credentials)
        self.connection = pika.BlockingConnection(parameters=connection_params)
        