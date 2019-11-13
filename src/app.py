from aiocqhttp import CQHttp
from datetime import datetime
from sendmsg import SendMsg
from loadData import LoadData
import threading
import time

# windows本机运行本脚本与coolq的配置
# HOST = '127.0.0.1'
# PORT = 7788

# docker的配置
HOST = '172.17.0.1'
PORT = 7788

# 固定不变
BASEURL = 'http://127.0.0.1:15700/'

bot = CQHttp(api_root=BASEURL)

d = {
    '博客': 'https://blog.csdn.net/qq20004604',
    'github': 'https://github.com/qq20004604',
    'nginx': 'https://github.com/qq20004604/nginx-demo',
    'django': 'https://github.com/qq20004604/Python3_Django_Demo',
    'docker': 'https://github.com/qq20004604/docker-learning',
    'webpack': 'https://github.com/qq20004604/webpack-study',
    'react': 'https://github.com/qq20004604/react-demo',
    'vue': 'github： https://github.com/qq20004604/vue-scaffold\n博客专栏（1.x）：https://blog.csdn.net/qq20004604/article/category/6381182',
    '笔记': 'https://github.com/qq20004604/notes',
    'demo': 'https://github.com/qq20004604/some_demo',
    '海外服务器': 'https://manage.hostdare.com/aff.php?aff=939\n这个可以做私人服务器（不需要备案），也可以找群主询问如何架设SS server的方法。',
    'QQ 机器人': 'https://github.com/qq20004604/qq-robot',
    '架构': 'https://juejin.im/post/5cea1f705188250640005472',
    'es6': 'https://blog.csdn.net/qq20004604/article/details/78014684',
    'vue 脚手架': 'https://github.com/qq20004604/Vue-with-webpack',
    'react 脚手架': 'https://github.com/qq20004604/react-with-webpack',
    'Macbook 上手攻略': 'https://github.com/qq20004604/when-you-get-new-Macbook',
    'python的 django 与 mysql 交互': 'https://blog.csdn.net/qq20004604/article/details/89934212'
}

ld = LoadData()


def log(context, filename='./log.log'):
    with open(filename, 'a', encoding='utf-8') as f:
        f.write('time:%s, sender:%s, message_type:%s, user_id:%s, content:%s\n' % (
            datetime.now(),
            context['sender']['nickname'],
            context['message_type'],
            context['sender']['user_id'],
            context['raw_message']))


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
    with open('./group.log', 'a', encoding='utf-8') as f:
        f.write(str(context) + '\n')

    return {'reply': result}


@bot.on_notice('group_increase')
async def handle_group_increase(context):
    await bot.send(context, message='欢迎新人～可以输入#help来向我查询所有命令喔',
                   at_sender=True, auto_escape=True)


@bot.on_request('group', 'friend')
async def handle_request(context):
    return {'approve': True}


SendMsg(BASEURL)


def mixin_dict():
    global d
    hour = 0
    while True:
        # 1 分钟更新一次
        time.sleep(60)
        hour = hour + 1
        print('%s hour pass' % hour)
        ld_dict = ld.load_search_info()
        d = {**d, **ld_dict}


t1 = threading.Thread(target=mixin_dict, name='loop')
t1.start()

bot.run(host=HOST, port=PORT)
