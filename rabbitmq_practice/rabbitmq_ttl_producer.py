import pika
import json

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost")
)

channel = connection.channel()

channel.basic_publish(
    exchange="",
    routing_key="ttl_csv",
    body=json.dumps({
        "filename": "temporary.csv"
    }),
    properties=pika.BasicProperties(
        delivery_mode=2
    )
)

print("Message published!")

connection.close()