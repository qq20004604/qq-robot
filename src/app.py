from aiocqhttp import CQHttp
from datetime import datetime
import datetime as dt
from apscheduler.schedulers.blocking import BlockingScheduler
import config
import threading

bot = CQHttp()

d = {
    '博客': 'https://blog.csdn.net/qq20004604',
    'github': 'https://github.com/qq20004604',
    'nginx': 'https://github.com/qq20004604/nginx-demo',
    'django': 'https://github.com/qq20004604/Python3_Django_Demo',
    'docker': 'https://github.com/qq20004604/docker-learning',
    'webpack': 'https://github.com/qq20004604/webpack-study',
    'react': 'https://github.com/qq20004604/react-demo',
    'vue': 'https://github.com/qq20004604/vue-scaffold',
    '笔记': 'https://github.com/qq20004604/notes',
    'demo': 'https://github.com/qq20004604/some_demo',
    '海外服务器': 'https://manage.hostdare.com/aff.php?aff=939',
}


def log(context, filename='./log.log'):
    with open(filename, 'a') as f:
        f.write('time:%s, sender:%s, message_type:%s, user_id:%s, content:%s\n' % (
            datetime.now(),
            context['sender']['nickname'],
            context['message_type'],
            context['sender']['user_id'],
            context['raw_message']))


def getGroupContxt(group_id=387017550):
    return {
        'anonymous': None,
        'font': 1473688,
        'group_id': group_id,
        'message': '',  # 现在应该可以了
        'message_id': 593,
        # 'message_type': 'group',
        # 'post_type': 'message',
        # 'raw_message': '',  # 现在应该可以了
        # 'self_id': 2691365658,
        # 'sender': {
        #     'age': 30,
        #     'area': '杭州',
        #     'card': '前阿里-零零水',
        #     'level': '传说',
        #     'nickname': '零零水',
        #     'role': 'owner',
        #     'sex': 'male',
        #     'title': '',
        #     'user_id': 20004604
        # },
        # 'sender': None,
        'sub_type': 'normal',
        'time': 0,  # 1558323327
        'user_id': 0  # 20004604
    }


@bot.on_message()
async def handle_msg(context):
    msg = context['message'].lower()

    '''
    # print(str(context)) 内容示例如下
     {'font': 1473688, 'message': '#help', 'message_id': 528, 'message_type': 'private', 'post_type': 'message',
     'raw_message': '#help', 'self_id': 2691365658,
     'sender': {'age': 30, 'nickname': '零零水', 'sex': 'male', 'user_id': 20004604}, 'sub_type': 'friend',
     'time': 1558283078, 'user_id': 20004604}
     '''

    result = ''
    isindict = False
    isinhelp = False
    for k in d:
        if ('#' + k) in msg:
            result += d[k] + '\n'
            isindict = True

    if '#help' in msg:
        result += '你可以使用以下命令~记得前面带上#喔\n'
        isinhelp = True
        for k in d:
            result += '#' + k + '\n'

    # 默认词典要求给star
    if isindict is True:
        result += "记得给star！"

    # 只要是词典之一，则打印日志
    if isindict is True or isinhelp is True:
        log(context)
    with open('./group.log', 'a') as f:
        f.write(str(context) + '\n')

    return {'reply': result}


@bot.on_notice('group_increase')
async def handle_group_increase(context):
    await bot.send(context, message='欢迎新人～',
                   at_sender=True, auto_escape=True)


@bot.on_request('group', 'friend')
async def handle_request(context):
    return {'approve': True}


def start():
    print('start')
    bot.send(getGroupContxt(), message='小秘书已启动～你可以通过例如【#help】（不含中括号）来查看全部命令～现在时间是 %s' % datetime.now(),
             auto_escape=True)


def run_thread():
    # 实例化一个调度器
    scheduler = BlockingScheduler()
    scheduler.add_job(start, 'date', run_date=(datetime.now() + dt.timedelta(seconds=5)), args=[])
    # 开始运行调度器
    scheduler.start()


t1 = threading.Thread(target=run_thread)
t1.setDaemon(True)
t1.start()

bot.run(host=config.HOST, port=config.PORT)

# print('before join')
# t.join(1)
# print('after join')
