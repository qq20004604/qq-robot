# qq-robot

[![License](https://img.shields.io/github/license/qq20004604/qq-robot.svg)](LICENSE)

QQ机器人，依赖于以下东西：

* 酷Q（使用docker版）：https://cqhttp.cc/docs/4.10/#/
* python-aiocqhttp：https://github.com/richardchien/python-aiocqhttp

部分教程参考：

* Nonebot：https://none.rclab.tk/guide/installation.html

## 1、安装

首先，在linux上跑酷Q的docker。

https://cqhttp.cc/docs/4.10/#/?id=%E4%BD%BF%E7%94%A8-docker

其次，在docker上配置好 CoolQ HTTP API 插件，这个略微麻烦一些，可能需要把docker里面app文件夹映射到外面来：

https://cqhttp.cc/docs/4.10/#/?id=%E6%89%8B%E5%8A%A8%E5%AE%89%E8%A3%85

第三，在docker里登录你的QQ（建议是小号QQ）。

第四，你还需要配置一下这个插件，确保酷Q的那个插件，和之后的python代码能交互，参考一下这个：

https://none.rclab.tk/guide/getting-started.html

第五，然后安装 python-aiocqhttp，其中 CQHttp 可以不带任何参数执行。

https://github.com/richardchien/python-aiocqhttp

第六，然后参考本项目里src文件夹中的config进行配置，运行 ``app.py`` 即可。

**验证：**

私聊你的小号QQ，内容和返回应该如下：

```
零零水  23:26:21
#help

小秘书  23:26:22
你可以使用以下命令~记得前面带上#喔
#博客
#github
#nginx
#django
#docker
#webpack
#react
#vue
#笔记
#demo
#海外服务器


```