import pika
import json

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost")
)

channel = connection.channel()

channel.queue_declare(
    queue="normal_csv",
    durable=True
)


def callback(ch, method, properties, body):
    message = json.loads(body)

    print(f"Received: {message['filename']}")
    print("Processing normal-priority CSV...")

    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(
    queue="normal_csv",
    on_message_callback=callback,
    auto_ack=False
)

print("Waiting for normal-priority messages...")

channel.start_consuming()