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
shanbei_send_group = driver.config.admin_group
BOT_ID = str(driver.config.bot_id)

shanbei = on_command("shanbei", aliases={'扇贝', }, priority=5, permission=permission.SUPERUSER)

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    'Host': "apiv3.shanbay.com",
    'Cookie': ""
}


@shanbei.handle()
async def _(bot: Bot, event: Event, state: T_State):
    try:
        ret = await is_check()
        await shanbei.send(message=ret)
    except:
        await shanbei.send(message='服务不可用', at_sender=True)


async def is_check():
    url = f'https://apiv3.shanbay.com/wordsapp/user_material_books/brtce/learning/statuses'

    async with aiohttp.ClientSession() as session:
        response = await session.get(url=url, headers = headers)
        response = await response.json()

    return '\n'.join([f"{j} : {k}" for j,k in response.items()])

