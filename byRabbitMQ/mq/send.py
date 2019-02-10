import pika
import sys
import settings

class BaseMQ:
    def __init__(self,user,pwd):
        '''
            实例化sender时，需要执行的操作：
                -1 指定用户名及密码
                -2 设置connection的一些参数
        '''
        self.credentials=pika.PlainCredentials(user,pwd)
        self.connection=None
        self.channel=None
        pass

    def createConnection(self,**kwargs):
        '''
            连接
        :return:
        '''
        host=kwargs.get('host')
        port=kwargs.get('port')
        # 连接参数
        parameters=pika.ConnectionParameters(host=host,port=port,credentials=self.credentials)
        if self.connection==None:
            self.connection=pika.BlockingConnection(parameters=parameters)

    def createChannel(self):
        '''
            创建通道
        :return:
        '''
        if self.channel==None:
            self.channel= self.connection.channel()
        pass

    def createBroker(self,exchange=None,exchange_type=None,durable=True):
        '''
            创建一个broker
        :return:
        '''
        # 指定一个交换机

        exchange= exchange if exchange is not None else ''
        type=exchange_type if exchange_type is not None else 'direct'
        self.channel.exchange_declare(exchange=exchange, exchange_type=type, durable=durable)

    def createQueue(self,name):
        '''
            声明一个队列
        :return:
        '''
        self.channel.queue_declare(queue=name)

    def close(self):
        '''
            关闭当前连接
        :return:
        '''
        self.connection.close()

class Sender(BaseMQ):
    '''
        不直接调用sender，由构造者调用
    '''
    # def __init__(self,user,pwd):
    #     '''
    #         实例化sender时，需要执行的操作：
    #             -1 指定用户名及密码
    #             -2 设置connection的一些参数
    #     '''
    #     self.credentials=pika.PlainCredentials(user,pwd)
    #     self.connection=None
    #     self.channel=None
    #     pass
    #
    # def createConnection(self,**kwargs):
    #     '''
    #         连接
    #     :return:
    #     '''
    #     host=kwargs.get('host')
    #     port=kwargs.get('port')
    #     # 连接参数
    #     parameters=pika.ConnectionParameters(host=host,port=port,credentials=self.credentials)
    #     if self.connection==None:
    #         self.connection=pika.BlockingConnection(parameters=parameters)
    #
    # def createChannel(self):
    #     '''
    #         创建通道
    #     :return:
    #     '''
    #     if self.channel==None:
    #         self.channel= self.connection.channel()
    #     pass
    #
    # def createBroker(self,exchange=None,exchange_type=None,durable=True):
    #     '''
    #         创建一个broker
    #     :return:
    #     '''
    #     # 指定一个交换机
    #
    #     exchange= exchange if exchange is not None else ''
    #     type=exchange_type if exchange_type is not None else 'direct'
    #     self.channel.exchange_declare(exchange=exchange, exchange_type=type, durable=durable)
    #
    # def createQueue(self,name):
    #     '''
    #         声明一个队列
    #     :return:
    #     '''
    #     self.channel.queue_declare(queue=name)
    #
    # def close(self):
    #     '''
    #         关闭当前连接
    #     :return:
    #     '''
    #     self.connection.close()

    def publish(self,msg,routing_key):
        '''
            发送消息
        :param msg:
        :return:
        '''
        self.channel.basic_publish(exchange='',routing_key=routing_key,body=msg)
        print(f"[x] sent {msg}")

class BaseBuilder:
    '''
        父类的构造者，为send以及receve两个子类的父类
    '''
    def __init__(self,user,pwd,host,port):
        self.builder=None
        self.user=user
        self.pwd=pwd
        self.host=host
        self.port=port

    def _construct_sender(self,queue_name):
        '''

        :param queue_name:
        :return:
        '''
        self.builder=Sender(self.user,self.pwd)
        [step for step in (
            self.builder.createConnection(host=self.host,port=self.port),
            self.builder.createChannel(),
            # self.builder.createBroker(),
            self.builder.createQueue(queue_name))]

class SenderBuilder:
    # def __init__(self,user,pwd,host,port):
    #     self.builder=None
    #     self.user=user
    #     self.pwd=pwd
    #     self.host=host
    #     self.port=port
    #
    # def _construct_sender(self,queue_name):
    #     '''
    #         使用建造者模式依次执行各方法，由send方法直接调用
    #     :param queue_name:
    #     :return:
    #     '''
    #     self.builder=Sender(self.user,self.pwd)
    #     [step for step in (
    #         self.builder.createConnection(host=self.host,port=self.port),
    #         self.builder.createChannel(),
    #         # self.builder.createBroker(),
    #         self.builder.createQueue(queue_name))]

    def send(self,queue_name,routing_key,msg):
        '''
            向rabbitmq发送消息
        :param queue_name:
        :param routing_key:
        :param msg:
        :return:
        '''
        self._construct_sender(queue_name)
        self.builder.publish(msg,routing_key)
        self.builder.close()

def test():
    '''
        测试Sender的创建
    :return:
    '''
    enginerr=SenderBuilder(settings.RABBITMQ_USER,settings.RABBITMQ_PWD,settings.RABBITMQ_HOST,settings.RABBITMQ_PORT)
    enginerr.send(settings.RABBITMQ_QUEUE,settings.RABBITMQ_ROUTING_KEY,'测试发送的消息')


# 以下代码暂时注释
# connection = pika.BlockingConnection(pika.ConnectionParameters(
#     host=settings.RABBITMQ_HOST))
# channel = connection.channel()
#
# channel.exchange_declare(exchange='logs',
#                          type='fanout')
#
#
# message = ' '.join(sys.argv[1:]) or "info: Hello World!"
# channel.basic_publish(exchange='logs',
#                       routing_key='',
#                       body=message)
# print(f" [x] Sent {message}")
# connection.close()