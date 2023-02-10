#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2021/8/4 17:31
# @Author      : Rubicon 
# @File        : mysql_week.py
# @PROJECT_NAME: 安全开发课程
# @Software    : PyCharm


import socket
from urllib import parse
import MySQLdb



passwd = ['','admin', '123456', 'huting','root', 'password', '123123', '123', '1', '', '{user}',
          '{user}{user}', '{user}1', '{user}123', '{user}2016', '{user}2015',
          '{user}!', 'P@ssw0rd!!', 'qwa123', '12345678', 'test', '123qwe!@#',
          '123456789', '123321', '1314520', '666666', 'woaini', 'fuckyou', '000000',
          '1234567890', '8888888', 'qwerty', '1qaz2wsx', 'abc123', 'abc123456',
          '1q2w3e4r', '123qwe', '159357', 'p@ssw0rd', 'p@55w0rd', 'password!',
          'p@ssw0rd!', 'password1', 'r00t', 'system', '111111', 'admin']

socket.setdefaulttimeout(1)  # socket超时设置


def get_vul_info():
    vul_info = {
        "type": "no_web",
        "author": "PgHook",
    }
    return vul_info


def bug_check(date):
    if 'http' in date:
        result = parse.urlparse(date)
        ip = str(result.netloc)
        ip = ip.split(':')[0]
    else:
        ip=date
    try:  # 判断端口是否开放
        socket.setdefaulttimeout(1)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, 3306))

        for pwd in passwd:
            try:
                pwd = pwd.replace('{user}', 'root')
                conn = MySQLdb.connect(ip, 'root', pwd, 'mysql')

                conn.close()
                vule_date = {'vule_name': 'Mysql存在弱口令', 'severity': 'high',
                             'vule_url': ip + ':3306  week_password: ' + pwd,
                             'url': date}
                print(vule_date)
                return vule_date
            except Exception as e:
                pass
    except:
        return

# bug_check('http://192.168.60.15')