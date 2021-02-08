import aiohttp
from nonebot import on_command, permission, get_driver
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot import require
scheduler = require('nonebot_plugin_apscheduler').scheduler


__plugin_name__ = ''
__plugin_usage__ = ''

now_state = None
driver = get_driver()
kaibo_send_group = driver.config.kaibo_send_group
BOT_ID = str(driver.config.bot_id)

douyu_1 = on_command("douyu_1", aliases={'银樰开播了吗', '开播了吗',}, priority=5)

@douyu_1.handle()
async def _(bot: Bot, event: Event, state: T_State):
    try:
        ret = await is_kaibo('5998143')
        await douyu_1.send(message=ret)
    except:
        await douyu_1.send(message='服务不可用', at_sender=True)

douyu_dabo = on_command("douyu_dabo", aliases={'开波了吗',}, priority=5)

@douyu_dabo.handle()
async def _(bot: Bot, event: Event, state: T_State):
    try:
        ret = await is_kaibo('4624967')
        await douyu_dabo.send(message=ret)
    except:
        await douyu_dabo.send(message='服务不可用', at_sender=True)

async def is_kaibo(rid):
    url = f'http://open.douyucdn.cn/api/RoomApi/room/{rid}'

    async with aiohttp.ClientSession() as session:
        response = await session.get(url=url)
        response = await response.json()

    if response['error'] != 0:
        return ('服务不可用')

    data = response['data']

    if data['room_status'] != '1':
        return ('未开播')

    return (
        f"已开播\n房间名: {data['room_name']}\n开始时间: {data['start_time']}\n房间链接: [CQ:share,url=https://www.douyu.com/room/share/{rid},title=女装樰]")

async def kaibo_notice():
    global now_state
    new_state = await is_kaibo('4624967')
    if now_state == '未开播':
        if new_state != now_state:
            bot = driver.bots[BOT_ID]
            await bot.send_group_msg(group_id=kaibo_send_group, message=new_state)
    now_state = new_state

scheduler.add_job(kaibo_notice, 'interval', seconds=300)