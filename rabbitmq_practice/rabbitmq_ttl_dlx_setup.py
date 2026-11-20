import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost")
)

channel = connection.channel()

channel.exchange_declare(
    exchange="failed_processing",
    exchange_type="direct",
    durable=True
)

channel.queue_declare(
    queue="failed_csv",
    durable=True
)

channel.queue_bind(
    exchange="failed_processing",
    queue="failed_csv",
    routing_key="failed"
)

channel.queue_declare(
    queue="ttl_csv_with_dlq",
    durable=True,
    arguments={
        "x-message-ttl": 10000,
        "x-dead-letter-exchange": "failed_processing",
        "x-dead-letter-routing-key": "failed"
    }
)

print("TTL + DLX infrastructure created!")

connection.close()