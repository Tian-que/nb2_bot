from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.adapters.cqhttp.message import Message

import aiohttp
from bs4 import BeautifulSoup
import random

__plugin_name__ = '斗图'
__plugin_usage__ = '指令：[来张表情包] 表情包主题'


doutu = on_command("doutu", aliases={'来张表情包','来个表情包','表情包', }, priority=5)

@doutu.handle()
async def _(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    if args:
        state['theme'] = args

@doutu.got('theme', prompt="表情包主题？")
async def _(bot: Bot, event: Event, state: T_State):
    theme = state['theme']
    try:
        ret = await get_img_url(theme)
        await doutu.send(message=Message(ret),at_sender=True)
    except:
        await doutu.send(message='服务不可用',at_sender=True)
    pass

async def get_img_url(theme):
    url = 'https://www.doutula.com/search?keyword=' + theme
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
    async with aiohttp.ClientSession() as session:
        response = await session.get(url = url,headers = headers)
        content = await response.read()
    soup = BeautifulSoup(content, 'lxml')
    all = soup.find_all('img', class_='img-responsive lazy image_dtb')
    img = [i['data-backup'] for i in all][:20]
    return '[CQ:image,file=' + random.choice(img) + ']'