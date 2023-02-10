#!/usr/bin/env python

import argparse
import sys
import os
from netaddr import IPSet


def get_ips(target):
    try:
        ips = []
        for ip in IPSet([target]):
            ips.append(str(ip))
        return ips
    except:
        return ips

def bug_list(file):
    poc_list = []
    for root, dirs, files in os.walk(file):
        for f in files:
            # file_path = os.path.join(root, f)
            if 'pyc' not in f:
                f = f.split('.')[0]
                poc_list.append(f)
    return poc_list


def cmdlineparser():
    parser = argparse.ArgumentParser(description='Powered by ChengS ',
                                     usage='python My_scanT.py -f sub_doamin.txt -t 10',
                                     add_help=True)

    parser.add_argument('-u', '--url', help='可以是指定要扫描目标url，也可以是ip或者ip段，支持子网掩码，如192.168.1.1/24')
    parser.add_argument('-f', '--file', help='从文件中读取扫描目标')
    parser.add_argument('-t', '--thread', type=int, help='扫描线程设置', default=1)
    parser.add_argument('-b', '--bug_plu', help='指定漏洞插件名称')
    parser.add_argument('-bl', '--bug_list',  default='False', action='store_true', help='列出漏洞插件列表')
    parser.add_argument('-T', '--type',  choices=['all', 'web', 'no_web'], default='all', help='指定调用插件类型,web:调用web类型插件;noweb:调用非web插件;all:所有插件。')

    if len(sys.argv) == 1:
        sys.argv.append('-h')
    return parser.parse_args()


