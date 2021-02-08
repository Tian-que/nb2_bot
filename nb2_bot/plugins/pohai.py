from nonebot import on_command, permission, get_driver
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.adapters.cqhttp.message import Message
from nonebot.adapters.cqhttp import GroupMessageEvent, GROUP_OWNER, GROUP_ADMIN
from nonebot.rule import Rule
from nonebot import require
from nb2_bot.utils import download_file
from nb2_bot.Rules import check_group_message
import asyncio
scheduler = require('nonebot_plugin_apscheduler').scheduler
import random, os
import time

__plugin_name__ = '随机迫害'
__plugin_usage__ = '指令：[随机迫害]'

driver = get_driver()
BOT_ID = str(driver.config.bot_id)

pohai = on_command("pohai", rule=check_group_message(),  aliases={'随机迫害', }, priority=5)

@pohai.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    try:
        img = os.listdir(os.path.join(os.getcwd(), 'nb2_bot', 'data', 'pohai', str(event.group_id)))
        fig_dir = os.path.join(os.getcwd(), 'nb2_bot', 'data', 'pohai', str(event.group_id)) + '\\' + random.choice(img)
        ret = '[CQ:image,file=file:///' + fig_dir + ']'
        await pohai.send(message=Message(ret))
    except:
        await pohai.send(message='当前群没有迫害名单')


pohai_add = on_command("pohai_add", rule=check_group_message(),  aliases={'添加迫害', }, priority=5, permission = GROUP_OWNER | GROUP_ADMIN)

@pohai_add.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    images = [seg.data.get('url') for seg in event.message if seg.type == "image"]
    ret = '添加成功'
    for image in images:
        figname = time.strftime("%Y_%m_%d%H_%M_%S", time.localtime()) + '.png'
        filename = os.path.join(os.getcwd(), 'nb2_bot', 'data', 'pohai', str(event.group_id), figname)
        await download_file(url=image,filename=filename)
        await asyncio.sleep(1)
        ret += '[CQ:image,file=file:///' + filename + ']'
    await pohai_add.send(message=Message(ret))

async def pohai_m():
    img = os.listdir(os.path.join(os.getcwd(), 'nb2_bot', 'data', 'pohai', '699721296'))
    fig_dir = os.path.join(os.getcwd(), 'nb2_bot', 'data', 'pohai', '699721296') + '\\' + random.choice(img)
    ret = '[CQ:image,file=file:///' + fig_dir + ']'
    bot = driver.bots[BOT_ID]
    await bot.send_group_msg(group_id=699721296, message=Message('早上好(冰心除外)\n' + ret))

scheduler.add_job(pohai_m, 'cron',hour=6,minute=0)