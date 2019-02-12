from conf import settings
from mq.send import BaseMQ,BaseBuilder
from core.models import *
from core.bll import *
# from core.log import logger
from log.log import MyLog


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
            print(f"[x] Received %r {body}")
            try:
                oceanData=OceanObservationgData(settings.WATCH_DIR,body)
                fubInfo = oceanData.fubInfo
                realtimeInfo = oceanData.realtimeInfo
                fub = BuoInfoBLL()
                realtime = RealtimeInfoBLL()
                fub_temp = fub.isExist(fubInfo.no)
                if fub_temp == None:
                    # 插入fubinfo，并返回插入后的（带有自增主键id的fubinfo）
                    fub_temp = fub.create(fubInfo)
                else:
                    pass
                # 插入realtimeinfo
                realtime.create(realtimeInfo, fub_temp, fubInfo.dt)
                # time.sleep(body.count('.'))
                # print(f"[x] 插入成功")
                # logger.info(f"[x] 插入成功")
                MyLog.addInfo(f"[~] {body}插入成功")
                print(f"[~] {body}插入成功")
                print('[x] Done')
            except Exception as ex:
                # print(ex)
                # logger.warn(f'[!] 解析失败{body}')
                MyLog.addWarn(f'[!] 解析失败{body}|错误原因:{ex}')
                # print(f"[!] 解析失败 {body}")
                print('[x] Error')

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

