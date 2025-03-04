import uuid
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
apps_client = client.AppsV1Api()

connection = pika.BlockingConnection(parameters=connection_params)
channel = connection.channel()
channel.queue_declare("work-queue")

def work_callback(ch, method, properties, body):
    resource_details = json.loads(body)
    config_id = str(uuid.uuid4())
    cu_config = helpers.make_cu_configmap(resource_details.core_ip,
                                         resource_details.core_port,
                                         config_id)
    kubernetes_client.create_namespaced_config_map(namespace="default", body=cu_config)
    deployment_config = helpers.make_deployment_config(config_id)
    try:
        apps_client.create_namespaced_deployment(namespace="default", body=deployment_config)
        print("deployment created")
    except client.exceptions.ApiException as e:
        print("deployment create failed")
        print(str(e))

channel.basic_consume(queue="work-queue",
                        on_message_callback=work_callback,
                        auto_ack=True)

channel.start_consuming()