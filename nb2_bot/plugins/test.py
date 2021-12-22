# coding=utf-8
from nonebot import on_command, on_message
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.adapters.cqhttp import GroupMessageEvent
from nb2_bot.utils.JsonIO import *
from nonebot.adapters.cqhttp.message import Message
from nonebot.adapters.cqhttp import utils
from nonebot.rule import Rule
import aiohttp
from bs4 import BeautifulSoup
import asyncio

import time
import csv

test = on_command("test", aliases={'测试', }, priority=5)


@test.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    try:
        node_message = [
            {
                "type": "node",
                "data": {
                    "name": "1",
                    "uin": "1",
                    "content": [
                        {
                            "type": "text",
                            "data": {"text": "3"}
                        }
                    ]
                }
            },
            {
                "type": "node",
                "data": {
                    "name": "1",
                    "uin": "1",
                    "content": [
                        {
                            "type": "text",
                            "data": {"text": "2"}
                        }
                    ]
                }
            },
            {
                "type": "node",
                "data": {
                    "name": "1",
                    "uin": "1",
                    "content": [
                        {
                            "type": "text",
                            "data": {"text": "1"}
                        }
                    ]
                }
            }]
        await bot.send_group_forward_msg(group_id=event.group_id, messages=node_message)
    except Exception as e:
        print(e)

test2 = on_command("xml_test", aliases={'生成卡片', }, priority=5)


@test2.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    url = "https://baike.baidu.com/item/%E5%82%BB%E9%80%BC/977754?fr=aladdin"
    # url = await json_escape(url)
    title = ""
    summary = ""
    cover = "http://gchat.qpic.cn/gchatpic_new/1605206150/694531998-2298333927-4BDDAB313FB24C25FEF8167A44CDC358/0?term=3"
    icon = "http://gchat.qpic.cn/gchatpic_new/1605206150/694531998-3129629945-4D48F97F9BB2A2230913AC7BD33E5F83/0?term=3"
    name = "百度分享"
    # group_id = 699721296
    #
    ree = ("<?xml version='1.0' encoding='UTF-8' standalone='yes'?><msg "
            'templateID="123" '
            f'url="{url}" '
            'serviceID="1" action="web" actionData="" a_actionData="" i_actionData="" '
            'brief="百度分享" flag="0"><item layout="2"><picture '
            f'cover="{cover}"/><title>{title}</title><summary>{summary}</summary></item><source '
            f'url="{url}" '
            f'icon="{icon}" '
            f'name="{name}" appid="0" action="web" actionData="" a_actionData="tencent0://" '
            'i_actionData=""/></msg>')
    #
    msg_id  = await test2.send(message=Message(f'[CQ:xml,data={ree}]'))
    await asyncio.sleep(3)
    await bot.delete_msg(message_id = msg_id['message_id'])


    #
    # xiaozhan_json = '{"app": "com.tencent.miniapp","desc":"",;"view":"notification,"ver":"0.0.0.1","prompt":"123","meta":{"notification":{"appInfo":{"appName":"9","appType":4,"appid":2034149631,},"data":[{"title":"1","value":"1"}]}}}'
    # xiaozhan_json = utils.escape(xiaozhan_json)
    # ret = f'[CQ:json,data={xiaozhan_json}]'
    # await test2.send(message=Message(ret))


async def json_escape(str):
    str = str.replace("&", "&amp;")
    str = str.replace(",", "&#44;")
    str = str.replace("[", "&#91;")
    str = str.replace("]", "&#93;")
    print(str)
    return str

# def check_recall() -> Rule:
#     async def _checker(bot: Bot, event: Event, state: T_State) -> bool:
#         if event.get_event_name() == 'notice.group_recall':
#             return True
#         return False
#     return Rule(_checker)
# rule=check_recall()


# anti_recall = on_message()
#
# @anti_recall.handle()
# async def _(bot: Bot, event: GroupMessageEvent):
#     d = 1
#     pass