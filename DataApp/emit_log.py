import base64
import pika
import sys

from DataApp.config import MessageBrokerConfig

connection = pika.BlockingConnection(pika.ConnectionParameters(host=MessageBrokerConfig.host,
                                                               port=MessageBrokerConfig.port))
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')

message = ' '.join(sys.argv[1:]) or "info: Hello World!"
channel.basic_publish(exchange='logs', routing_key='', body=base64.b64encode(bytes(str(message))))
print(f" [x] Sent {message}")
connection.close()
