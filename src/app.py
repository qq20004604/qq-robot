from aiocqhttp import CQHttp
from datetime import datetime
from sendmsg import SendMsg
from loadData import LoadData
import threading
import time

# windows本机运行本脚本与coolq的配置
# HOST = '127.0.0.1'
# PORT = 7788


# 这个url是发送给docker容器里的coolq
# 举例来说，假如docker命令有这样的 -p 3542:9000 -p 15700:5700
# 9000 是coolq暴露的页面访问地址（这里映射到了外面的3542，所以外界通过3542端口访问）
# 而5700是是coolq接受数据的端口（即是这个python服务发送给coolq的数据），这里映射到了15700，
# 所以外界通过15700端口发送信息给coolq
BASEURL = 'http://127.0.0.1:15700/'

bot = CQHttp(api_root=BASEURL)

d = {
    # '博客': 'https://blog.csdn.net/qq20004604',
    # 'github': 'https://github.com/qq20004604',
    # 'nginx': 'https://github.com/qq20004604/nginx-demo',
    # 'django': 'https://github.com/qq20004604/Python3_Django_Demo',
    # 'docker': 'https://github.com/qq20004604/docker-learning',
    # 'webpack': 'https://github.com/qq20004604/webpack-study',
    # 'react': 'https://github.com/qq20004604/react-demo',
    # 'vue': 'github： https://github.com/qq20004604/vue-scaffold\n博客专栏（1.x）：https://blog.csdn.net/qq20004604/article/category/6381182',
    # '笔记': 'https://github.com/qq20004604/notes',
    # 'demo': 'https://github.com/qq20004604/some_demo',
    # '海外服务器': 'https://manage.hostdare.com/aff.php?aff=939\n这个可以做私人服务器（不需要备案），也可以找群主询问如何架设SS server的方法。',
    # 'QQ 机器人': 'https://github.com/qq20004604/qq-robot',
    # '架构': 'https://juejin.im/post/5cea1f705188250640005472',
    # 'es6': 'https://blog.csdn.net/qq20004604/article/details/78014684',
    # 'vue脚手架': 'https://github.com/qq20004604/Vue-with-webpack',
    # 'react脚手架': 'https://github.com/qq20004604/react-with-webpack',
    # 'Macbook常用软件': 'https://github.com/qq20004604/when-you-get-new-Macbook',
    # 'python的django与mysql交互': 'https://blog.csdn.net/qq20004604/article/details/89934212'
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
    msg = context['message']
    # print(msg)
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
    minutes = 0
    while True:
        # 1 分钟更新一次
        minutes = minutes + 1
        if minutes % 60 == 0:
            print('%s hours pass' % (minutes / 60))
        ld_dict = ld.load_search_info()
        d = {**ld_dict}
        time.sleep(60)


t1 = threading.Thread(target=mixin_dict, name='loop')
t1.start()

# docker的配置
HOST = '172.18.0.1'
PORT = 12399

# 这里是coolq接收到qq信息，然后发送到这个python服务的端口。
# 所以也就是这个python服务，接收到这个消息的端口
# 在 coolq 的docker容器里，这个是在 */coolq/app/io.github.richardchien.coolqhttpapi/config/(qq号).ini 里配置的
# 由于容器不能通过 127.0.0.1 直接访问宿主机的端口，因此，需要通过执行 ip addr show docker0 命令来查看宿主机的端口
# 举例来说，我的server执行这个命令，获得的宿主机的 ip 是 172.18.0.1 （即，容器访问 172.18.0.1 这个地址是访问宿主机）
# 于是修改那个ini配置文件：post_url = http://172.18.0.1:34519
# 这里的host可以保持要和那个ip地址保持一样，port也是
bot.run(host=HOST, port=PORT)
