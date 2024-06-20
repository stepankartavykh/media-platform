from enum import Enum
import base64
import pika

from DataApp.config import MessageBrokerConfig


class MessageNotification(Enum):
    failure = 0
    success = 1


class MessageBrokerService:
    @staticmethod
    def send_message(message: str, message_id: int = None) -> MessageNotification:
        with pika.BlockingConnection(pika.ConnectionParameters(host=MessageBrokerConfig.host.value,
                                                               port=MessageBrokerConfig.port.value)) as connection:
            channel = connection.channel()

            channel.queue_declare(queue='task_queue', durable=True)

            channel.basic_publish(exchange='',
                                  routing_key='task_queue',
                                  body=base64.b64encode(message.encode('utf-8')),
                                  properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent))
            message_log_id = message_id if message_id else id(message)
            print(f" [x] Sent {message_log_id}")
        return MessageNotification.success


if __name__ == '__main__':
    MessageBrokerService.send_message("test 1244")
