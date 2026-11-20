import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost")
)

channel = connection.channel()

channel.exchange_declare(
    exchange="file_processing",
    exchange_type="direct",
    durable=True
)

channel.exchange_declare(
    exchange="failed_processing",
    exchange_type="direct",
    durable=True
)

channel.queue_declare(
    queue="high_priority_csv",
    durable=True,
    arguments={
        "x-dead-letter-exchange": "failed_processing",
        "x-dead-letter-routing-key": "failed"
    }
)

channel.queue_declare(
    queue="normal_csv",
    durable=True
)

channel.queue_declare(
    queue="failed_csv",
    durable=True
)

channel.queue_bind(
    exchange="file_processing",
    queue="high_priority_csv",
    routing_key="high"
)

channel.queue_bind(
    exchange="file_processing",
    queue="normal_csv",
    routing_key="normal"
)

channel.queue_bind(
    exchange="failed_processing",
    queue="failed_csv",
    routing_key="failed"
)

print("RabbitMQ infrastructure configured successfully!")

connection.close()