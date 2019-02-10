import sys
from conf import settings
from mq.send import SenderBuilder
from mq.receive import ReceiveBuilder


def main():
    params=sys.argv[1:]
    print(params)
    if len(params)==0 or params[0]!='send':
        enginerr = ReceiveBuilder(settings.RABBITMQ_USER, settings.RABBITMQ_PWD, settings.RABBITMQ_HOST,
                                  settings.RABBITMQ_PORT)
        enginerr.receive(settings.RABBITMQ_QUEUE, settings.RABBITMQ_ROUTING_KEY)
    elif params[0]=='send':
        enginerr = SenderBuilder(settings.RABBITMQ_USER, settings.RABBITMQ_PWD, settings.RABBITMQ_HOST,
                                 settings.RABBITMQ_PORT)
        enginerr.send(settings.RABBITMQ_QUEUE, settings.RABBITMQ_ROUTING_KEY, '测试发送的消息')


if __name__=='__main__':
    main()
