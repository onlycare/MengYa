#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2021/8/3 18:03
# @Author      : Rubicon 
# @File        : 漏洞扫描插件模板.py
# @PROJECT_NAME: 安全开发课程
# @Software    : PyCharm

import requests

def bug_check(url):

    try:
        res = requests.get(url, timeout=5, verify=False)
        if 'server.port' in res.text:
            vule_date = {'vule_name': 'sprintboot env', 'severity': 'high', 'vule_url': url, 'url': url}
            return vule_date
    except:
        pass