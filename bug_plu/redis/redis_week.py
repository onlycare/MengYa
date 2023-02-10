#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2021/8/4 16:48
# @Author      : Rubicon 
# @File        : redis_week.py
# @PROJECT_NAME: 安全开发课程
# @Software    : PyCharm

import socket
import random
import time
from urllib import parse

PASSWORD_DIC = ['redis', 'root', 'oracle', 'password', 'p@aaw0rd', 'abc123!', '123456', 'admin', '12345678', '666666',
                '88888888', '1234567890', '888888']
socket.setdefaulttimeout(1)  # socket超时设置
ports = ['6379', '6380', '6377', '6389', '6369']


def get_vul_info():
    vul_info = {
        "type": "no_web",
        "author": "PgHook",
    }
    return vul_info


def bug_check(date):

    if 'http' in date:
        result = parse.urlparse(date)
        ip = str(result.netloc)  # 192.168.1.1:8080
        ip = ip.split(':')[0]
    else:
        ip=date

    for port in ports:
        try:
            socket.setdefaulttimeout(1)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, int(port)))
            s.send("INFO\r\n".encode('utf-8'))

            result = s.recv(1024)
            if "redis_version" in result.decode():
                time.sleep(random.random())
                vule_date = {'vule_name': 'redis unauthorized', 'severity': 'high', 'vule_url': ip+':'+port, 'url': date}

                print(vule_date)
                return vule_date

            elif "Authentication" in result.decode():
                for pass_ in PASSWORD_DIC:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((ip, int(port)))
                    pa = "AUTH %s\r\n" % (pass_)
                    s.send(pa.encode('utf-8'))
                    result = s.recv(1024)
                    if '+OK' in result.decode():
                        time.sleep(random.random())
                        vule_date = {'vule_name': 'redis week_password', 'severity': 'high', 'vule_url': ip + ':' + port+'  week_password: '+pass_,
                                     'url': date}
                        print(vule_date)
                        return vule_date

        except:
            pass


# bug_check('192.168.0.106')