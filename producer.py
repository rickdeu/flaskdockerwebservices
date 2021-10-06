import pika, os, json

url = os.environ.get('CLOUDAMQP_URL', 'amqps://pzjgbwsb:ciEtFIUV1iX3Kd66mmi9HW0fAuBXOukQ@beaver.rmq.cloudamqp.com/pzjgbwsb')

params = pika.URLParameters(url)
#params = pika.URLParameters('amqps://pzjgbwsb:ciEtFIUV1iX3Kd66mmi9HW0fAuBXOukQ@beaver.rmq.cloudamqp.com/pzjgbwsb')

connection = pika.BlockingConnection(params)
#connection = pika.BlockingConnection(params)

channel = connection.channel() # start a channel
#channel = connection.channel()



def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='admin', body = json.dumps(body), properties = properties)
