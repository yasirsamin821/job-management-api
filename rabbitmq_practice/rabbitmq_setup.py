import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost')
)

channel = connection.channel()

channel.exchange_declare(
    exchange='file_processing',
    exchange_type='direct',
    durable=True
)


channel.queue_declare(
    queue="high_priority_csv",
    durable=True
)


channel.queue_declare(
    queue='normal_csv',
    durable=True
)

channel.queue_bind(
    exchange='file_processing',
    queue='high_priority_csv',
    routing_key='high'
)

channel.queue_bind(
    exchange='file_processing',
    queue='normal_csv',
    routing_key='normal'
)

print('RabbitMQ setup complete')
connection.close()

