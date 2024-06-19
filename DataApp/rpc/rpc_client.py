import base64

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
                                   body=base64.b64encode(bytes(str(n))))
        while self.response is None:
            self.connection.process_data_events(time_limit=None)
        if isinstance(self.response, int):
            return int(self.response)
        raise Exception('Response is not integer!')


fibonacci_rpc = FibonacciRpcClient()

print(" [x] Requesting fib(30)")
response = fibonacci_rpc.call(30)
print(f" [.] Got {response}")
