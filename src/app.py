from aiocqhttp import CQHttp
import config

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


def log(msg):
    with open('./log.log', 'a') as f:
        f.write(msg + '\n')


@bot.on_message()
async def handle_msg(context):
    msg = context['message'].lower()
    print(msg)
    result = ''
    for k in d:
        if ('#' + k) in msg:
            result += d[k] + '\n'

    if '#help' in msg:
        result += '你可以使用以下命令~记得前面带上#喔\n'
        for k in d:
            result += '#' + k + '\n'

    return {'reply': result}


@bot.on_notice('group_increase')
async def handle_group_increase(context):
    await bot.send(context, message='欢迎新人～',
                   at_sender=True, auto_escape=True)


@bot.on_request('group', 'friend')
async def handle_request(context):
    return {'approve': True}


bot.run(host=config.HOST, port=config.PORT)
