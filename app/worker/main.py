import json
import os
import pika
from dotenv import load_dotenv
load_dotenv()
from kubernetes import client, config
import helpers

connection_credentials = pika.PlainCredentials(username=os.getenv("RABBITMQ_USERNAME"),
                                                password=os.getenv("RABBITMQ_PASSWORD"))
connection_params = pika.ConnectionParameters(
                                                host=os.getenv("RABBITMQ_BROKER"),
                                                port=os.getenv("RABBITMQ_PORT"),
                                                credentials=connection_credentials,
                                                heartbeat=300)

config.load_incluster_config()

kubernetes_client = client.CoreV1Api()

connection = pika.BlockingConnection()
channel = connection.channel()
channel.queue_declare("work-queue")

def work_callback(ch, method, properties, body):
    resource_details = json.loads(body)
    du_config = helpers.make_du_manifest(resource_details.core_ip,
                                         resource_details.core_port)
    if helpers.create_pod(kubernetes_client, du_config):
        channel.basic_publish(exchange="",
                                routing_key="work-queue",
                                body="")

channel.basic_consume(queue="work-queue",
                        on_message_callback=work_callback,
                        auto_ack=True)

channel.start_consuming()