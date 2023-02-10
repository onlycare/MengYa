#!/usr/bin/env python

import os
import sys
from cmdline import cmdlineparser, bug_list
from cmdline import get_ips
import threadpool
import csv


def get_poc_list(file):
    poc_list = []
    for root, dirs, files in os.walk(file):
        for f in files:
            file_path = os.path.join(root, f)
            poc_list.append(file_path)
    return poc_list


def file_read(filename):
    url_list = []
    if 'csv' in filename:  # oneforall
        with open(filename) as f:
            reader = csv.DictReader(f)
            for i in reader:
                url_list.append(i['url'])
    else:
        with open(filename, encoding='utf-8') as f:
            date = f.readlines()
            for i in date:
                url = i.split('\n')[0]
                url_list.append(url)
    return url_list


def save_callback(request, result):
    try:
        if result:
            with open('result.txt', 'a', encoding='utf-8') as f:
                f.write(str(result) + '\n')
    except:
        pass


def scan(poc, url_list, thread):
    taskpool = threadpool.ThreadPool(thread)
    # 生成任务请求队列
    requests = threadpool.makeRequests(poc.bug_check, url_list, save_callback)
    # 将任务放到线程池中开始执行
    for req in requests:
        taskpool.putRequest(req)
    # 等待所有任务执行完成
    taskpool.wait()


def main():
    args = cmdlineparser()
    type = args.type

    if args.bug_list == True:  # 获取poc列表
        poc_list = bug_list('.\\bug_plu')
        for i in poc_list:
            print(i)
        sys.exit()


    elif args.file == None:
        if '/' in args.url:  # 针对ip段
            target_list = get_ips(args.url)
        else:                # 针对单个url
            target_list = []
            target_list.append(args.url)
    else:  # 从文件中读取目标
        file_name = args.file
        target_list = file_read(file_name)

    thread = args.thread
    poc_list = get_poc_list('.\\bug_plu')
    if args.bug_plu != None:  # 是否指定poc扫描
        poc_name = args.bug_plu
    else:
        poc_name = None

    for bug in poc_list:
        if '__pycache__' in bug or 'pyc' in bug:
            pass
        else:
            script_name = bug.split('.')[1].rsplit('\\', 1)[1]
            path = bug.split('.')[1].rsplit('\\', 1)[0]

            sys.path.append(sys.path[0] + path)
            poc = __import__(script_name)
            if poc_name != None:  # 是否指定poc扫描
                if script_name == poc_name:
                    print('调用{}插件扫描'.format(script_name))
                    scan(poc, target_list, thread)
            elif type == poc.get_vul_info()['type'] or type == 'all':
                print('调用{}插件扫描'.format(script_name))
                scan(poc, target_list, thread)

            # else:
            #     if args.type == 'all':
            #         print('调用{}插件扫描'.format(script_name))
            #         scan(poc, target_list, thread)
            #     elif args.type == poc.get_vul_info()['type']:
            #         print('调用{}插件扫描'.format(script_name))
            #         scan(poc, target_list, thread)


if __name__ == "__main__":
    main()
