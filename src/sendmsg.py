import requests
import threading
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import datetime as dt
import time
import urllib.parse


# 开始时通报
def start_notice():
    # pass
    return {
        # 这个是群号，你改成自己机器人加入的那个群就行了
        'group_id': 387017550,
        'message': '小秘书已启动～你可以通过例如【#help】（不含中括号）来查看全部命令～现在时间是 %s' % time.strftime("%Y-%m-%d %H:%M:%S.%m",
                                                                                  time.localtime())
    }


# 定期执行通报
def inter_notice():
    return {
        'group_id': 387017550,
        'message': '小秘书 is running～你可以通过例如【#help】（不含中括号）来查看全部命令～现在时间是 %s' % time.strftime("%Y-%m-%d %H:%M:%S.%m",
                                                                                          time.localtime())
    }


class SendMsg(object):
    def __init__(self, BASEURL):
        # 单次触发事件，执行完即移除
        self.event_pool = [
            {
                'action': 'send_group_msg',
                'data': start_notice
            },

            # {
            #     'action': 'send_private_msg',
            #     'data': {
            #         'user_id': 20004604,
            #         'message': '小秘书已启动～你可以通过例如【#help】（不含中括号）来查看全部命令～现在时间是 %s' % datetime.now()
            #     }
            # }
        ]
        # 轮询触发事件，一直保持存在。这里的参数都需要执行函数来获取，以确保是最新的内容
        self.interval_pool = [
            {
                'action': 'send_group_msg',
                'data': inter_notice
            }
            # {
            #     'action': 'send_private_msg',
            #     'data': inter_notice
            # }
        ]
        # 上一次触发时间
        self.last_emit_time = datetime.now()

        self.BASEURL = BASEURL

        # 开一个新线程，执行定期清空 event_pool
        t1 = threading.Thread(target=self.loop)
        t1.setDaemon(True)
        t1.start()

        # 再开一个新线程，执行定时器（暂略）
        t2 = threading.Thread(target=self.run_interval)
        t2.setDaemon(True)
        t2.start()

    # 轮询
    def loop(self):
        # 先休眠2秒再开始执行
        time.sleep(4)
        if len(self.event_pool) > 0:
            # 两次发送间隔不小于2秒
            if datetime.now() > self.last_emit_time + dt.timedelta(milliseconds=2000):
                self.deal_loop_event()

    # 事件处理
    def deal_loop_event(self):
        e = self.event_pool.pop(0)
        try:
            # 数据是实时获取的
            data = e['data']()
            if e['action'] == 'send_group_msg':
                self.send_group_msg(data['group_id'], data['message'])
            elif e['action'] == 'send_private_msg':
                self.send_private_msg(data['user_id'], data['message'])
        except BaseException as e:
            print(str(e))
            pass
        finally:
            self.last_emit_time = datetime.now()

    # 定期执行事件的查询
    def interval_loop(self):
        # 先休眠2秒再开始执行
        time.sleep(5)
        if len(self.interval_pool) > 0:
            # 两次发送间隔不小于2秒
            if datetime.now() > self.last_emit_time + dt.timedelta(milliseconds=2000):
                self.deal_interval_loop_event()

    # 定期执行
    def deal_interval_loop_event(self):
        for e in self.interval_pool:
            try:
                # 数据是实时获取的
                data = e['data']()
                if e['action'] == 'send_group_msg':
                    self.send_group_msg(data['group_id'], data['message'])
                elif e['action'] == 'send_private_msg':
                    self.send_private_msg(data['user_id'], data['message'])
            except BaseException as e:
                print(str(e))
                pass
            finally:
                self.last_emit_time = datetime.now()

    # 私聊发送信息
    def send_private_msg(self, user_id, msg):
        # 需要 urllib.parse.quote(msg) 进行转义，不然例如 # 这种会被直接识别为哈希地址的表示。
        url = '%ssend_private_msg?user_id=%s&message=%s' % (self.BASEURL, user_id, urllib.parse.quote(msg))
        ret = requests.post(url)
        # 发送成功
        if ret.status_code == 200:
            pass
        else:
            print('send error: %s' % ret.reason)
        # self.bot.send_group_msg(group_id=387017550, message=msg)

    # 群聊发送信息
    def send_group_msg(self, group_id, msg):
        url = '%ssend_group_msg?group_id=%d&message=%s' % (self.BASEURL, group_id, urllib.parse.quote(msg))
        print(url)
        ret = requests.post(url)
        # 发送成功
        if ret.status_code == 200:
            pass
        else:
            print('send error: %s' % ret.reason)

    def run_interval(self):
        # 实例化一个调度器
        scheduler = BlockingScheduler()
        scheduler.add_job(self.interval_loop, 'interval', hours=6,
                          start_date=datetime(datetime.now().year, datetime.now().month, datetime.now().day,
                                              datetime.now().hour))
        # 开始运行调度器
        scheduler.start()


# 测试代码和示例代码
if __name__ == '__main__':
    pass
