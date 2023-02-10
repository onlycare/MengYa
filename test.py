#!/usr/bin/env python
# -*- coding: utf-8 -*-


# from urllib import parse
#
# #url解码
#
# urldata = 'https://www.cnblogs.com/xiao-xue-di/p/11843371.html'
#
#
# #url结果
# result = parse.urlparse(urldata)
# print(result)
# print(result.netloc)

import pymysql

try:
    db = pymysql.connect(host="192.168.83.246",
                         user="root",
                         password="root",
                         port=3306,#int not str
                         database="mysql",
                         charset='utf8')

    cursor = db.cursor()
    print('asasdsad')
except Exception as e:
    print('error:', e)