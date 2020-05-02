import requests
import threading
import time
import urllib.parse


# 开始时通报
def start_notice():
    # pass
    return {
        # 这个是群号，你改成自己机器人加入的那个群就行了
        'group_id': 387017550,
        'message': '小秘书已启动～你可以通过例如【#help】（不含中括号）来查看全部命令～现在时间是 %s' % time.strftime("%Y-%m-%d %H:%M:%S",
                                                                                  time.localtime())
    }


# 定期执行通报
def inter_notice():
    return {
        'group_id': 387017550,
        # 'user_id': 20004604,
        'message': '小秘书 is running～你可以通过例如【#help】（不含中括号）来查看全部命令～现在时间是 %s' % time.strftime("%Y-%m-%d %H:%M:%S",
                                                                                          time.localtime())
    }


class SendMsg(object):
    def __init__(self, base_url):
        # 基础路径
        self.base_url = base_url
        # 事件池
        self.event_pool = [
            {
                # 行为（这个是api）
                'action': 'send_group_msg',
                # 发送数据，这是一个函数，取返回值，是一个dict，拼接这个dict生成url
                'event_data': start_notice,
                # 最近一次发送时间，发送后更新为当前时间time.time()，这个单位是秒
                'last_send_time': 0,
                # 发送间隔，单位秒
                'sent_duration': 3600,
                # 发送次数。5表示发送5次，-1 代表无限次
                'remain_times': 1
            },
            {
                # 行为（这个是api）
                'action': 'send_private_msg',
                # 发送数据，这是一个函数，取返回值
                'event_data': inter_notice,
                # 最近一次发送时间，发送后更新为当前时间time.time()
                'last_send_time': 0,
                # 发送间隔（6个小时一次）
                'sent_duration': 3600 * 6,
                # 发送次数。5表示发送5次，-1 代表无限次
                'remain_times': -1
            },
        ]

        # 开一个新线程，定期执行轮询
        t1 = threading.Thread(target=self.loop)
        t1.setDaemon(True)
        t1.start()

    # 轮询
    def loop(self):
        while True:
            t = time.time()
            for event in self.event_pool:
                # 如果和上次发送时间间隔，大于设置的时间间隔
                if t - event['last_send_time'] > event['sent_duration']:
                    # 剩余触发次数不为0
                    if event['remain_times'] != 0:
                        # 触发事件
                        self.run_event(event)
                        # 剩余次数减一
                        event['remain_times'] -= 1
                        # 修改当前触发事件的最后触发事件
                        event['last_send_time'] = t
                        # 每次触发事件后，则延迟5秒
                        time.sleep(5)
            # print('loop')
            # 每秒轮询一次
            time.sleep(1)

    # 执行时间
    def run_event(self, event_data):
        try:
            # 数据是实时获取的
            data = event_data['event_data']()
            if event_data['action'] == 'send_group_msg':
                self.send_group_msg(data['group_id'], data['message'])
            elif event_data['action'] == 'send_private_msg':
                self.send_private_msg(data['user_id'], data['message'])
        except BaseException as e:
            print(str(e))

    # 私聊发送信息
    def send_private_msg(self, user_id, msg):
        # 需要 urllib.parse.quote(msg) 进行转义，不然例如 # 这种会被直接识别为哈希地址的表示。
        url = '%ssend_private_msg?user_id=%s&message=%s' % (self.base_url, user_id, urllib.parse.quote(msg))
        ret = requests.post(url)
        print(url)
        # 发送成功
        if ret.status_code == 200:
            print('ret.status_code: %s' % ret.status_code)
        else:
            print('send error: %s' % ret.reason)
        # self.bot.send_group_msg(group_id=387017550, message=msg)

    # 群聊发送信息
    def send_group_msg(self, group_id, msg):
        url = '%ssend_group_msg?group_id=%d&message=%s' % (self.base_url, group_id, urllib.parse.quote(msg))
        print(url)
        ret = requests.post(url)
        # 发送成功
        if ret.status_code == 200:
            print('ret.status_code: %s' % ret.status_code)
        else:
            print('send error: %s' % ret.reason)


# 测试代码和示例代码
if __name__ == '__main__':
    pass
