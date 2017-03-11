#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging,json,sys,time,requests,os,re,random,urllib
from qqbot import QQBot
reload(sys)
sys.setdefaultencoding( "utf-8" )

request_timeout=5

def mstimestamp():
    return int(round(time.time() * 1000))

header={
    'Cookie':'BAIDUID=',
    'User-Agent':'User-Agent:Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
}
def tracking(query,retry=0):
    try:
        api_addr="https://sp0.baidu.com/9_Q4sjW91Qh3otqbppnN2DJv/pae/channel/data/asyncqury"
        payload = {
            'cb': '',
            'appid': 4001,
            'nu': query,
            'vcode' : '',
            'token' : '',
            '_' : mstimestamp()
            }
        req_raw = requests.get(api_addr,params=payload,headers=header)
        req_json = req_raw.json();
        if(retry>=5):
            return "查询失败!错误:-5"
        elif(req_json['status']=='0'):
            timeArray = time.localtime(int(req_json['data']['info']['context'][0]['time']))
            uptime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            return "[%s]%s"%(uptime,req_json['data']['info']['context'][0]['desc'])
        elif(req_json['status']=='-5'):
            if(len(req_raw.cookies)>=1):
                header['Cookie']="BAIDUID=%s"%(req_raw.cookies['BAIDUID'])
            return tracking(query,retry+1)
        else:
            return req_json['msg']
    except ValueError:
        return "查询接口爆炸"
    except requests.exceptions.Timeout as e:
        return "垃圾百度"

def weather(city):
    try:
        api_addr = "http://wthrcdn.etouch.cn/weather_mini"
        payload ={
            'city' : city
        }
        req_json = requests.get(api_addr,params=payload).json();
        if req_json['status'] == 1000 :
            return "%s°C %s"%(req_json['data']['wendu'],req_json['data']['ganmao'])
        else:
            return "无可奉告"
    except ValueError:
        return "这垃圾API原地爆炸了"
    except requests.exceptions.Timeout as e:
        return "这垃圾API根本没法用"



myqqbot = QQBot()

@myqqbot.On('qqmessage')
def handler(bot, message):
    #输出帮助
    if message.content == '--help':
        #bot.Send('buddy', uin=message.memberUin, content='hello')
        bot.SendTo(message.contact, '某10的辣鸡bot，使用世界上最好的语言编写\n--wd [城市名] 查气温\n--joke 讲个笑话\n--news 讲个大新闻\n--cnm 操你妈不会百度吗\n--kuaidi [单号] 查快递\n--gay [对方名字] 检测一个人是不是gay\n--help 并没有卵用的帮助\n--stop 望咩啊')
    #停止bot
    elif message.content == '--stop':
        if(message.contact.qq == '1034825603'):
            bot.SendTo(message.contact, 'bye!')
            bot.Stop()
        else:
            bot.SendTo(message.contact, '滚')
    elif message.content == '--joke':
        bot.SendTo(message.contact, '无可奉告')
    elif message.content == '--news':
        bot.SendTo(message.contact, '无可奉告')
    #查快递
    elif message.content[:8] == '--kuaidi':
        if len(message.content[8:]) > 32:
            return bot.SendTo(message.contact, "滚")
        kuaidi_query = re.findall(r'(\w*[0-9]+)\w*',message.content[8:])
        if len(kuaidi_query)>0 :
            bot.SendTo(message.contact,tracking(kuaidi_query,retry=0))
    #检测一个人是不是GAY
    elif message.content[:5] == '--gay':
        isGay = random.randint(0,1)
        if isGay :
            bot.SendTo(message.contact,"%s是GAY"%(message.content[5:].strip()))
        else :
            bot.SendTo(message.contact,"%s好像不是GAY"%(message.content[5:].strip()))
    #操你妈不会百度吗
    elif message.content[:5] == '--cnm':
        urlKW=urllib.quote(message.content[5:].strip())
        bot.SendTo(message.contact,"cnm不会百度吗?\nhttps://www.baidu.com/s?wd=%s"%(urlKW))
    #查温度
    elif message.content[:4] == '--wd':
        city=message.content[4:].strip()
        bot.SendTo(message.contact,weather(city))

myqqbot.LoginAndRun()
