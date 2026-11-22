import pika
import json

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)

channel = connection.channel()

channel.confirm_delivery()

messages = [
    {
        'routing_key': 'high',
        'filename': 'important.csv'
    },
    {
        'routing_key': 'high',
        'filename': 'regular.csv'
    },
    {
        'routing_key': 'high',
        'filename': 'urgent.csv'
    }
]

for message in messages:
    routing_key = message['routing_key']

    body = json.dumps({
        'filename': message['filename'],
    })

    try:
        channel.basic_publish(
            exchange='file_processing',
            routing_key=routing_key,
            body=body,
            mandatory=True,
            properties=pika.BasicProperties(
                delivery_mode=2
            )
        )

        print(f"Published: {message['filename']} -> {routing_key}")

    except pika.exceptions.UnroutableError:
        print(f"Unroutable: {message['filename']} -> {routing_key}")

connection.close()