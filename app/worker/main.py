import uuid
import json
import os
import pika
from dotenv import load_dotenv
load_dotenv()
from kubernetes import client, config
import helpers
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

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
    try:
        logger.info("message received")
        resource_details = json.loads(body)
        config_id = str(uuid.uuid4())
        cu_config = helpers.make_configmap(resource_details["core_ip"],
                                                resource_details["core_port"],
                                                config_id)
        kubernetes_client.create_namespaced_config_map(namespace="default", body=cu_config)
        deployment_config = helpers.make_deployment_config(config_id)
        try:
            apps_client.create_namespaced_deployment(namespace="default", body=deployment_config)
            logger.info("deployment %s created", str(config_id))
            
            response_body = json.dumps({
                "id": config_id,
                "message": "OK"
            })
            
            channel.basic_publish(
                exchange="",
                routing_key=properties.reply_to,
                properties=pika.BasicProperties(
                    correlation_id=properties.correlation_id
                ),
                body=response_body.encode("utf-8")
            )
            channel.basic_ack(delivery_tag=method.delivery_tag)
        except client.exceptions.ApiException as e:
            logger.error("deployment create failed: %s", str(e))
    except Exception as e:
        logger.error("error in work_callback %s", str(e))

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue="work-queue",
                        on_message_callback=work_callback)
logger.info("worker started")
channel.start_consuming()