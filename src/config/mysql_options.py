#!/usr/bin/env python3
# -*- coding: utf-8 -*-

mysql_config = {
    'database': 'qq_robot',
    # 这里是通过 docker network ls找到数据库的那个network，再通过 docker network inspect [mysql-network] 找到其对应的 ip
    'host': '172.19.0.1',
    'user': 'robot_inquirer',
    'port': 55001,
    'pw': '213723123fewfewfwefew!@$@!feq_1'
}

# redis_config = {
#     'host': '',
#     'port': 0,
#     'decode_responses': True,
#     'password': ''
# }
