from main import *
import pika, os, json

url = os.environ.get('CLOUDAMQP_URL', 'amqps://pzjgbwsb:ciEtFIUV1iX3Kd66mmi9HW0fAuBXOukQ@beaver.rmq.cloudamqp.com/pzjgbwsb')

params = pika.URLParameters(url)
#params = pika.URLParameters('amqps://pzjgbwsb:ciEtFIUV1iX3Kd66mmi9HW0fAuBXOukQ@beaver.rmq.cloudamqp.com/pzjgbwsb')

connection = pika.BlockingConnection(params)
#connection = pika.BlockingConnection(params)

channel = connection.channel() # start a channel
#channel = connection.channel()

channel.queue_declare(queue='main') # Declare a queue
#channel.queue_declare(queue='main')



def callback(ch, method, properties, body):
    print('Received in main')
    data = json.loads(body)
    print(body)

    if properties.content_type == 'product_created':
        product = Product(id = data['id'], title=data['title'], image = data['image'])
        db.session.add(product)
        db.session.commit()
        print('Product created')

    elif properties.content_type == 'product_updated':
        product = Product.query.get(data['id'])
        product.title = data['title']
        product.image = data['image']
        db.session.commit()
        print('Product updated')

    elif properties.content_type == 'product_delete':
        product = Product.query.get(data)
        db.session.delete(product)
        db.session.commit()
        print('Product delete')




#channel.basic_consume('hello', callback, auto_ack=True)
channel.basic_consume(queue='main', on_message_callback=callback, auto_ack = True)

print('Started Consuming')

channel.start_consuming()

channel.close()
