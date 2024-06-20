import base64
import random
import sys
import time

import pika
import uuid

from DataApp.config import MessageBrokerConfig


class FibonacciRpcClient:

    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=MessageBrokerConfig.host.value,
                                                                            port=MessageBrokerConfig.port.value))
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(queue=self.callback_queue,
                                   on_message_callback=self.on_response,
                                   auto_ack=True)
        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_queue',
                                   properties=pika.BasicProperties(reply_to=self.callback_queue,
                                                                   correlation_id=self.corr_id),
                                   body=base64.b64encode(str(n).encode()))
        while self.response is None:
            self.connection.process_data_events(time_limit=3)
        if isinstance(self.response, int):
            return int(self.response)
        elif isinstance(self.response, bytes):
            try:
                return int(self.response)
            except ValueError:
                return str(self.response)
        raise Exception('Response is not integer!', str(self.response))


def process_args() -> int:
    args = sys.argv
    if len(args) == 1:
        print("Enter value for rpc client!")
        sys.exit()
    elif len(args) > 2:
        print("Too many arguments!")
        sys.exit()
    return int(args[1])


def main():
    value = process_args()
    fibonacci_rpc_client = FibonacciRpcClient()
    while True:
        try:
            val = value + random.randint(30, 35)
            print(f" [x] Requesting fib({val})")
            response = fibonacci_rpc_client.call(val)
            time.sleep(1)
            print(f" [.] Got {response}")
        except KeyboardInterrupt:
            print('\nEnough!')
            break


if __name__ == '__main__':
    main()
