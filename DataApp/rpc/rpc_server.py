import base64

import pika

from DataApp.config import MessageBrokerConfig

connection = pika.BlockingConnection(pika.ConnectionParameters(host=MessageBrokerConfig.host.value,
                                                               port=MessageBrokerConfig.port.value))

channel = connection.channel()

channel.queue_declare(queue='rpc_queue')


def calc_fib_number(n) -> int:
    def fib(number: int) -> int:
        if number == 0:
            return 0
        elif number == 1:
            return 1
        else:
            return fib(number - 1) + fib(number - 2)
    print(f'processing fib({n})...')
    result = fib(n)
    print('end')
    return result


def on_request(ch, method, props, body):
    n = int(base64.b64decode(body))

    print(f" [.] fib({n})")
    response = calc_fib_number(n)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id=props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='rpc_queue', on_message_callback=on_request)

print(" [x] Awaiting RPC requests")
channel.start_consuming()
