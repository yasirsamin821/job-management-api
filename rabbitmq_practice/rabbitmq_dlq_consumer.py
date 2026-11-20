import pika
import json

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost")
)

channel = connection.channel()

channel.queue_declare(
    queue="failed_csv",
    durable=True
)


def callback(ch, method, properties, body):
    message = json.loads(body)

    print("Received failed message!")
    print(f"Filename: {message['filename']}")

    print("Sending message for investigation...")

    ch.basic_ack(
        delivery_tag=method.delivery_tag
    )


channel.basic_consume(
    queue="failed_csv",
    on_message_callback=callback,
    auto_ack=False
)

print("Waiting for failed messages...")

channel.start_consuming()