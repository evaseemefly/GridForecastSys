import pika


# 1 建立一个到RabbitMQ服务器的连接，设置指定参数
connection=pika.BlockingConnection(pika.ConnectionParameters('localhost',5672))

#
channel=connection.channel()

# 2 先创建一个名为hello的队列，若发送消息前队列不存在，rb会抛弃这条消息！
channel.queue_declare(queue='hello')

# 3 使用默认交换机（exchange）
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello world')

print('已发送')
# 3 关闭连接
connection.close()