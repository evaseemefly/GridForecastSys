from conf import settings
from mq.send import BaseMQ,BaseBuilder
from core.models import *

class Receiver(BaseMQ):


    def consume(self,routing_key):
        '''
            消费者方法
        :param routing_key:
        :return:
        '''
        def callback(ch, method, properties, body):
            '''
                触发的回调函数，通过该回调函数，实现对文件的读取操作
            :param ch:
            :param method:
            :param properties:
            :param body:
            :return:
            '''
            if isinstance(body, bytes):
                body = str(body, encoding="utf-8")
            print(f" [x] Received %r {body}")
            oceanData=OceanObservationgData(settings.WATCH_DIR,body)
            fubInfo = oceanData.fubInfo
            realtimeInfo = oceanData.realtimeInfo

            # time.sleep(body.count('.'))
            print('[x] Done')

        self.channel.basic_consume(callback,
                              queue=routing_key,
                              no_ack=True)
        self.channel.start_consuming()

class ReceiveBuilder(BaseBuilder):
    # def __init__(self,user,pwd,host,port):
    #     self.builder=None
    #     self.user=user
    #     self.pwd=pwd
    #     self.host=host
    #     self.port=port
    #
    def _construct_sender(self,queue_name):
        self.builder=Receiver(self.user,self.pwd)
        [step for step in (
            self.builder.createConnection(host=self.host,port=self.port),
            self.builder.createChannel(),
            # self.builder.createBroker(),
            self.builder.createQueue(queue_name))]

    def receive(self,queue_name,routing_key):
        self._construct_sender(queue_name)
        self.builder.consume(routing_key)
        self.builder.close()

def test():
    enginerr = ReceiveBuilder(settings.RABBITMQ_USER, settings.RABBITMQ_PWD, settings.RABBITMQ_HOST,
                              settings.RABBITMQ_PORT)
    enginerr.receive(settings.RABBITMQ_QUEUE, settings.RABBITMQ_ROUTING_KEY)

