from nonebot import on_command, get_driver
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot import require
scheduler = require('nonebot_plugin_apscheduler').scheduler

import binascii
import socket
import time
import asyncio

__plugin_name__ = 'DNF体验服大区状态'
__plugin_usage__ = '指令：体验服'

driver = get_driver()
TYF_STATE_PUSH_LIST = driver.config.tyf_state_push_list
BOT_ID = str(driver.config.bot_id)

Region = {
    "天界": {
        "ip": "exp.tcls.qq.com",
        "port": 8080,
        "一区": 419,
        "二区": 575
    },
    "格兰": {
        "ip": "testd.tcls.qq.com",
        "port": 5001,
        "一区": 423,
        "二区": 597
    },
    "魔界": {
        "ip": "testf.tcls.qq.com",
        "port": 5005,
        "一区": 419,
        "二区": 575
    }
}

now_state = []

tyf = on_command("tyf", aliases={'体验服',}, priority=5)

@tyf.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    try:
        ret = [await is_open(name=k, **v) for k, v in Region.items()]
        await tyf.send(
            message='[查询] ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n' + '\n'.join(j for i in ret for j in i))
    except:
        await tyf.send(message='服务不可用', at_sender=True)


async def is_open(name, ip, port, **kwargs):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    s.send(binascii.a2b_hex("0a05641a0000000000200b010000177100000001000000000000"))
    #binascii.a2b_hex("0a05641a0000000000200b010000177100000001000000000000")
    rec = s.recv(1024)
    rec = binascii.b2a_hex(rec).decode()
    ret = []
    for k, v in kwargs.items():
        if rec[v] == '0':
            ret.append(f"{name}{k}:关")
        else:
            ret.append(f"{name}{k}:开")
    s.close()
    return ret


async def state_notice():
    global now_state
    ret = [await is_open(name=k, **v) for k, v in Region.items()]
    new_state = [j for i in ret for j in i]
    if now_state:
        if new_state != now_state:
            mes = '[服务器状态] ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            for i in range(len(now_state)):
                if now_state[i] != new_state[i]:
                    mes += f"\n{new_state[i].split(':')[0]}已{new_state[i].split(':')[1]}服"
            for group in TYF_STATE_PUSH_LIST:
                bot = driver.bots[BOT_ID]
                await bot.send_group_msg(group_id=group, message=mes)
                # await Bot.call_api(api="send_group_msg", message="hello world")
                await asyncio.sleep(1)
    now_state = new_state

scheduler.add_job(state_notice, 'interval', seconds=10)