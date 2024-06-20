import base64
import time

import pika
from pika.adapters.blocking_connection import BlockingConnection

# def send():
#     with pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672)) as connection:
#         channel = connection.channel()
#         channel.queue_declare(queue='hello')
#         channel.basic_publish(exchange='',
#                               routing_key='hello',
#                               body=base64.b64encode(b'Hello World!'))
#         print(" [x] Sent 'Hello World!'")


def hello_world():
    with pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672)) as connection:
        channel = connection.channel()
        channel.queue_declare(queue='task_queue')
        for i in range(10):
            channel.basic_publish(exchange='',
                                  routing_key='hello',
                                  body=base64.b64encode(f'Hello World! {i}'.encode()))
            time.sleep(1)
        print(channel.channel_number)
        print(channel.channel_number)
        second_channel = connection.channel()
        print(second_channel.channel_number)
        print(" [x] Sent 'Hello World!'")


if __name__ == '__main__':
    hello_world()
