import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from mq.send import SenderBuilder
from conf import settings

path='/Users/evaseemefly/Documents/01project/GridForecastSys/byRabbitMQ/watcherDir'

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        '''
            当监听到有创建的文件时，将fullpath推送至rabbitmq中的watcher_files 队列中
        :param event:
        :return:
        '''
        # if event.is_directory:
        print(f'[x] 事件类型：{event.event_type}|路径：{event.src_path}')
        # 将获取到的文件全路径及事件类型（创建-删除等）写入日志中
        # 将全路径推送至rabbitmq- watcher_files队列中
        enginer=enginerr = SenderBuilder(settings.RABBITMQ_USER, settings.RABBITMQ_PWD, settings.RABBITMQ_HOST,
                                 settings.RABBITMQ_PORT)
        enginerr.send(settings.RABBITMQ_QUEUE, settings.RABBITMQ_ROUTING_KEY, event.src_path)



if __name__=='__main__':
    event_handler=MyHandler()
    observer=Observer()
    observer.schedule(event_handler,path=path,recursive=True)
    observer.start()

    try:
        print('[*] 启动监听程序')
        print(f'[*] 监听路径为：{path}')
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()