import pika
import json

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost")
)

channel = connection.channel()

channel.queue_declare(
    queue="high_priority_csv",
    durable=True,
    arguments={
        "x-dead-letter-exchange": "failed_processing",
        "x-dead-letter-routing-key": "failed"
    }
)
import time

def callback(ch, method, properties, body):
    message = json.loads(body)

    print(f"Received: {message['filename']}")

    time.sleep(5)

    print("Processing successful!")

    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(
    queue="high_priority_csv",
    on_message_callback=callback,
    auto_ack=False
)

print("Waiting for high-priority messages...")

channel.start_consuming()