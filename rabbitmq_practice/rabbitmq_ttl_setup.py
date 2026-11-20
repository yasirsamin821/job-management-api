import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost")
)

channel = connection.channel()

channel.queue_declare(
    queue="ttl_csv",
    durable=True,
    arguments={
        "x-message-ttl": 10000
    }
)

print("TTL queue created!")

connection.close()