# -*- coding: utf-8 -*-
#Made by Fires

#前言
print('''Bilibili Followers Observer is an open-source program. Please check out the details at github.com/FiresJoeng/BFO
© 2023 Fires Young. All rights reserved.
This is an unstable version. Current version: v0.1b
''')
print('''B站粉丝监视器是一个开源的软件，请前往github.com/FiresJoeng/BFO了解详情。
© 2023 Fires Young. 最终解释权归Fires所有。
这是一个测试版。当前版本为：Beta 0.1
''')

#注入模块
import requests
import json
import time
import datetime
import os
import pathlib
import webbrowser

#文件检测
try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    path = pathlib.Path(current_dir)
    if not path.joinpath("config.ini").exists():
        print('未找到配置文件，正在生成配置文件中......')
        with open(path.joinpath("config.ini"), "w", encoding="utf-8") as create_config:
            create_config.write('''{
"bili_uid":"",
"delay_time":"",
"version":"0b1001101001011000010110001"
}''')
    current_dir = os.path.dirname(os.path.abspath(__file__))
    path = pathlib.Path(current_dir)
    if not path.joinpath("output.txt").exists():
        print('未找到输出文本，正在生成输出文本中......')
        with open(path.joinpath("output.txt"), "w") as t:
            t.write('')
    print('BFO初始化完毕！\nTwitter: @FiresYoung, GitHub: FiresJoeng')
except Exception as e:
    print('警告：发生了错误，错误类型：'+e+'\n程序即将退出，请检查文件检测问题或寻求开发者帮助，然后再以管理员身份重新启动本程序！')
    exit()

#更新检测
print('请稍等，BFO正在检测更新......')
repo_url = "https://github.com/FiresJoeng/BFO"
repo_api = "https://api.github.com/repos/FiresJoeng/BFO"
try:
    response = requests.get(repo_api)
    if response.status_code != 200:
        print('警告：服务器返回值不合法："+response.status_code+"\n程序即将退出，请检查服务器状态，并联系开发者！')
        exit()
    else:
        pass
    updated_at = json.loads(response.text)["updated_at"]
    orig_gittime = datetime.datetime.strptime(updated_at, "%Y-%m-%dT%H:%M:%SZ")
    gitver = bin(int(orig_gittime.strftime("%Y%m%d")))
except Exception as e:
    print('警告：发生了错误，错误类型："+e+"\n程序即将退出，请检查网络问题或寻求开发者帮助，然后再重新启动本程序！')
    exit()
try:
    with open("config.ini", "r", encoding="utf-8") as read_config:
        config_content = json.load(read_config)
        localver = config_content["version"]
    if gitver != localver:
        while True:
            update_selector = str(input('有新版本可用：\n[0]忽略 [1]前往更新页面 [2]永久忽略此新版本\n请输入单个数字来决定选项。\n>>> '))
            if update_selector == '0':
                print('这次启动已忽略更新。')
                break
            if update_selector == '1':
                print('即将前往更新页面......')
                webbrowser.open(repo_url)
                break
            if update_selector == '2':
                print('已永久忽略此新版本的更新，下一次提醒在新的更新版本到来时。')
                config_content["version"] = gitver
                with open("config.ini", "w", encoding="utf-8") as write_config:
                    json.dump(config_content, write_config)
                break
            else:
                print('请输入有效值！')
    else:
        print('目前暂无更新，或者有新的更新被忽略。当前软件版本：v0.1b')
except (json.JSONDecodeError, TypeError, ValueError, UnicodeError, AttributeError):
    print('警告：配置文件已损坏！请按任意键退出程序，然后再打开本程序一次！')
    os.remove(str(path) + '\config.ini')
    exit()

#定义监视
try:
    with open("config.ini", "r", encoding="utf-8") as read_config:
        config_content = json.load(read_config)
        uid = config_content["bili_uid"]
        if uid == '':
            while True:
                uid = input('看起来你是第一次使用这个脚本，那么请告诉我你要监视的UID >>> ')
                if uid:
                    try:
                        uid = int(uid)
                    except ValueError:
                        print('非法内容，请重新输入！')
                    else:
                        uid = str(uid)
                        break
                else:
                    print('输入的内容为空，请重新输入！')
            config_content["bili_uid"] = uid
            with open("config.ini", "w", encoding="utf-8") as write_config:
                json.dump(config_content, write_config)
        else:
            refill_uid = str(input('脚本记住了你上次输入的UID：{}。\n如果你需要监视新的UID，请输入“r”并回车（不包含双引号）；\n如果不需要，请随意输入内容并回车。\n请注意！脚本只会记住你最近一次监视的UID。\n>>> '.format(uid)))
            if refill_uid == 'r':
                while True:
                    uid = input('那么请告诉我你要监视的新的UID >>> ')
                    if uid:
                        try:
                            uid = int(uid)
                        except ValueError:
                            print('非法内容，请重新输入！')
                        else:
                            uid = str(uid)
                            break
                    else:
                        print('输入的内容为空，请重新输入！')
                config_content["bili_uid"] = uid
                with open("config.ini", "w", encoding="utf-8") as write_config:
                    json.dump(config_content, write_config)
            else:
                print('那么，脚本将继续监视UID:{}'.format(uid))
except (json.JSONDecodeError, TypeError, ValueError, UnicodeError, AttributeError):
    print('警告：配置文件已损坏！请按任意键退出程序，然后再打开本程序一次！')
    os.remove(str(path) + '\config.ini')
    exit()

#定义延迟
try:
    with open("config.ini", "r", encoding="utf-8") as read_config:
        config_content = json.load(read_config)
        time_delay = config_content["delay_time"]
        if time_delay == '':
            while True:
                time_delay = input('看起来你还没有设置过监视间隔，良好的监视间隔将防止出现未知的错误。\n请先设置监视间隔（单位：秒）\n>>> ')
                if time_delay:
                    try:
                        time_delay = int(time_delay)
                    except ValueError:
                        print('非法内容，请重新输入！')
                    else:
                        time_delay = str(time_delay)
                        break
                else:
                    print('输入的内容为空，请重新输入！')
            config_content["delay_time"] = time_delay
            with open("config.ini", "w", encoding="utf-8") as write_config:
                json.dump(config_content, write_config)
        else:
            refill_delay = str(input('脚本记住了你上次输入的监视间隔：{}秒。\n如果你需要监视新的UID，请输入“r”并回车（不包含双引号）；如果不需要，请随意输入内容并回车。\n请注意！脚本只会记住你最近一次的监视间隔。\n>>> '.format(time_delay)))
            if refill_delay == 'r':
                while True:
                    time_delay = input('那么请告诉我你要设置的新间隔 >>> ')
                    if time_delay:
                        try:
                            time_delay = int(time_delay)
                        except ValueError:
                            print('非法内容，请重新输入！')
                        else:
                            time_delay = str(time_delay)
                            break
                    else:
                        print('输入的内容为空，请重新输入！')
                config_content["delay_time"] = time_delay
                with open("config.ini", "w", encoding="utf-8") as write_config:
                    json.dump(config_content, write_config)
            else:
                print('那么，脚本将继续以每{}秒监视一次的频率开始检测。'.format(time_delay))
except (json.JSONDecodeError, TypeError, ValueError, UnicodeError, AttributeError):
    print('警告：配置文件已损坏！请按任意键退出程序，然后再打开本程序一次！')
    os.remove(str(path) + '\config.ini')
    exit()

#监视开始
time_delay = int(time_delay)
print('监视已开始，请在使用期间保持脚本的运行。\n监视结果将输出至脚本目录下的output.txt。\n如果需要结束监视，请直接关闭脚本窗口。')
biliuser_api = str('https://api.bilibili.com/x/relation/stat?vmid={}&jsonp=jsonp'.format(uid))
while True:
    try:
        response = requests.get(biliuser_api)
        data = json.loads(response.text)["data"]
        if response.status_code != 200:
            print('警告：服务器返回值不合法：'+response.status_code+'\n程序即将退出，请检查服务器状态和UID输入，然后再重新启动本程序！')
            exit()
        else:
            follower = str(data['follower'])    
            with open("output.txt", "w") as t:
                t.write(follower)
            time.sleep(time_delay)
    except Exception as e:
        print('警告：发生了错误，错误类型：'+e+'\n程序即将退出，请检查网络问题或寻求开发者帮助，然后再重新启动本程序！')
        exit()
