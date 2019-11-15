#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from mysql_lingling import MySQLTool


class LoadData(object):
    def __init__(self):
        self.mysql_config = None
        self._load_config()

    # 加载 mysql 配置
    def _load_config(self):
        try:
            from config.mysql_options import mysql_config
            self.mysql_config = mysql_config
        except ImportError:
            mysql_config = {
                'database': '',
                'host': '',
                'user': '',
                'port': 0,
                'pw': ''
            }
            print('无法加载到账号密码，请按代码中提供的格式')

    # 从 MySQL 加载数据
    def _load_from_mysql(self):
        if self.mysql_config is None:
            return None

        # 连接数据库
        with MySQLTool(host=self.mysql_config['host'],
                       user=self.mysql_config['user'],
                       password=self.mysql_config['pw'],
                       port=self.mysql_config['port'],
                       database=self.mysql_config['database']) as mtool:
            result = mtool.run_sql([
                [
                    'SELECT * FROM info'
                ]
            ])
            print(result)
            return result

    # 返回处理后的 dict
    def load_search_info(self):
        result = self._load_from_mysql()
        if result is None:
            return {}

        d = {}
        for row in result:
            d[row[1]] = row[2]
        return d
