import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5671))
channel = connection.channel()

channel.close()
