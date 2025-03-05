import uuid
import json
import os
import pika
from dotenv import load_dotenv
load_dotenv()
from kubernetes import client, config
import helpers
import logging
from prometheus_client import Counter, Summary, start_http_server

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

work_counter = Counter("number_of_commands_success",
                        "Number of commands successfully processed")
error_counter = Counter("number_of_commands_errors",
                        "Number of errors encountered when processing commands.")
processing_time = Summary("command_processing_time",
                          "Time spent processing a command.")

@processing_time.time()
def work_callback(ch, method, properties, body):
    with error_counter.count_exceptions():
        response_body = None
        try:
            logger.info("message received")
            resource_details = json.loads(body)
            if resource_details["command"] == "create":
                data = resource_details["data"]
                config_id = str(uuid.uuid4())
                cu_config = helpers.make_configmap(data["core_ip"],
                                                data["core_port"],
                                                config_id)
                kubernetes_client.create_namespaced_config_map(namespace="default", body=cu_config)
                deployment_config = helpers.make_deployment_config(config_id)
                try:
                    apps_client.create_namespaced_deployment(namespace="default", body=deployment_config)
                    logger.info("deployment %s created", str(config_id))
                    
                    response_body = {
                        "status": "ok",
                        "data": {
                            "id": config_id,
                            "message": "resources created"
                        }
                    }
                    work_counter.inc()
                except client.exceptions.ApiException as e:
                    logger.error("deployment create failed: %s", str(e))
                    response_body = {
                        "status": "error",
                        "data": {
                            "message": str(e)
                        }
                    }
            else:
                deployment_id = resource_details["data"]["resource_id"]
                apps_client.delete_namespaced_deployment(f"srsran-{deployment_id}", namespace="default")
                response_body = {
                    "status": "ok",
                    "data": {
                        "message": "resource deleted"
                    }
                }
                work_counter.inc()
        except Exception as e:
            logger.error("error in work_callback %s", str(e))
            response_body = {
                "status": "error",
                "data": {
                    "message": str(e)
                }
            }
        finally:
            channel.basic_publish(
                exchange="",
                routing_key=properties.reply_to,
                properties=pika.BasicProperties(
                    correlation_id=properties.correlation_id
                ),
                body=json.dumps(response_body).encode("utf-8")
            )
            channel.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue="work-queue",
                        on_message_callback=work_callback)
logger.info("worker started")
start_http_server(8080)
logger.info("metrics server started")
channel.start_consuming()