# qq-robot

[![License](https://img.shields.io/github/license/qq20004604/qq-robot.svg)](LICENSE)

QQ机器人，依赖于以下东西：

* 酷Q（使用docker版）：https://cqhttp.cc/docs/4.10/#/
* python-aiocqhttp：https://github.com/richardchien/python-aiocqhttp

部分教程参考：

* Nonebot：https://none.rclab.tk/guide/installation.html

接付费定制版QQ机器人，联系（QQ：20004604，微信：qq20004604，加的时候请注明来意）

### 说明

文件：

* app.py：主文件，启动它就行了；
* loadData.py：用于异步加载数据，避免每次更改数据后都重启 app.py 文件；
* sendmsg.py：理想中是自动定时推送信息，但目前有bug，不能正常推送，可以不引入；
* private.sql：创建数据库的sql文件，配合 loadData.py 使用；
* config/mysql_options.py：未上传文件，这个是连接mysql数据库的隐私文件，可以不引入，直接改 loadData.py 里的值就行；


先理解整个流程：

1. 流程一消息机器人：①coolq收到qq的消息（群、个人）；②通过 12399（自己定的）的端口推送给python服务；③消息服务拿到后，进行处理，再推送回 coolq；
2. 流程二主动推送：①coolq设置监听的端口（默认是5700）；②docker映射到相同或不同端口（参考下面的15700）；③python服务推送消息到其ip和端口；④coolq推送消息给用户；

执行顺序：

1. 查看宿主机的地址，参考 https://cloud.tencent.com/developer/ask/109551 这个地址在 app.py 的 HOST 要用
2. 找一个不冲突的端口，可以用我给的 12399（如果冲突你就换一个）；
3. BASEURL = 'http://127.0.0.1:15700/'，记住这个端口（端口下面要用），干嘛用的请看 app.py 的注释，或者上面流程解释；
4. 先执行本项目的 app.py。如果不需要异步加载数据库，就不要引入执行 ``loadData.py`` ，直接写死就行；
5. 记住这个地址，然后开始搞 coolq 的 docker 容器（命令在下面）；
6. 启动docker后，网页访问（访问不了就是防火墙问题），登录你的qq机器人（不要登大号，用小号）；
7. 都做完后，私聊一下你的小号，看看能不能正常回复信息；
8. 如果还不行，就自己再琢磨一下，参考链接都有给；
9. 琢磨不懂，付费找我咨询吧（QQ：20004604，微信：qq20004604，加的时候请注明来意），50~300元一次，包会；


### 启动命令

创建docker网络

```
docker network create qq_robot
```

```
docker pull richardchien/cqhttp:latest      // 拉取镜像
// 以下命令是一行里执行，这里分开写是为了方便用户理解
docker run -ti --name qqrobot
    --net=qq_robot  // 加入 qq_robot 网络
    -v $(pwd)/coolq:/home/user/coolq    // 持久化，方便配置。宿主目录就是当前执行目录/coolq目录
    -p 3542:9000    // 9000是web网页控制的访问地址，映射到3542，通过宿主机的3542端口访问。
    -p 15700:5700   // 5700是5700是coolq接受数据的端口（即是这个python服务发送给coolq的数据）
    -e COOLQ_ACCOUNT=12345678     // 这个是qq机器人的账号，填写后，会自动重新启动（注意，但第一次你还需要自己去访问网页输入密码登录机器人，这里只是断线后会自动登）
    -e VNC_PASSWD=1654879wddgfg     // 这个是web访问网页的密码，不填则是默认密码
    -e CQHTTP_POST_URL=http://172.18.0.1:12399  // 这个是coolq收到qq消息后，发送到哪个服务器进行处理。先创建好后，再写这个，也可以后续配置
    richardchien/cqhttp:latest  // 这个是使用的镜像
```

如果正常的话，执行完上面的命令会显示以下内容（示例）

```
[2020-05-01 17:15:28.663] [I] [日志] 日志控制台开启成功
[2020-05-01 17:15:28.672] [I] [HTTP] 开启 HTTP 服务器成功，开始监听 http://[::]:5700
[2020-05-01 17:15:28.687] [I] [HTTP] 通过 HTTP 上报数据到 http://172.18.0.1:12399 成功，状态码：204
[2020-05-01 17:15:35.203] [I] [HTTP] 通过 HTTP 上报数据到 http://172.18.0.1:12399 成功，状态码：200
```

这个时候你访问网页地址，登录你的机器人账号（不要用大号）就可以了。


## 安装（过时）

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


### sql

> 建表（需要root权限执行）

```
create schema if not exists qq_robot collate utf8mb4_general_ci;
create table if not exists info
(
	id int default 0 not null
		primary key,
	search_key varchar(40) null,
	search_result varchar(255) null,
	constraint info_search_key_uindex
		unique (search_key)
);
```

> 添加权限（密码仅供参考，需要和loadData.py里的一样）

```
GRANT ALL ON qq_robot.* to qq_rotbot_user@'%' IDENTIFIED BY '213123123fewfewfwefew';
FLUSH PRIVILEGES;
```