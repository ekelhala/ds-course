import os
import pika
from dotenv import load_dotenv
load_dotenv()

connection_credentials = pika.PlainCredentials(username=os.getenv("RABBITMQ_USERNAME"),
                                                password=os.getenv("RABBITMQ_PASSWORD"))
connection_params = pika.ConnectionParameters(
                                                host=os.getenv("RABBITMQ_BROKER"),
                                                port=os.getenv("RABBITMQ_PORT"),
                                                credentials=connection_credentials,
                                                heartbeat=300)

connection = pika.BlockingConnection()
channel = connection.channel()
channel.queue_declare("work-queue")

def work_callback(ch, method, properties, body):
    print(f"received {body}")

channel.basic_consume(queue="work-queue",
                        on_message_callback=work_callback,
                        auto_ack=True)

channel.start_consuming()