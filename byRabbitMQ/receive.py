
import pika
import time


credentials = pika.PlainCredentials('guest','guest')
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost',5672,'/',credentials))
channel = connection.channel()
channel.queue_declare(queue='hello')
print(f' [*] Waiting for messages. To exit press CTRL+C')
def callback(ch, method, properties, body):
    if isinstance(body,bytes):
        body = str(body, encoding="utf-8")
    print(f" [x] Received %r {body}")

    time.sleep(body.count('.'))
    print('[x] Done')
channel.basic_consume(callback,
                      queue='hello',
                      no_ack=True)
channel.start_consuming()