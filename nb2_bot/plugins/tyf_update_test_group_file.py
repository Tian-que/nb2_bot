from nonebot import get_driver, on_notice
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
# from nonebot.adapters.cqhttp.event import NoticeEvent
from nonebot import require
scheduler = require('nonebot_plugin_apscheduler').scheduler

from nonebot.rule import Rule
from nb2_bot.utils import download_file

def check_tyf_file() -> Rule:
    async def _checker(bot: Bot, event: Event, state: T_State) -> bool:
        if event.notice_type == 'group_upload' and event.group_id == tyf_file_group_id:
            return True
        else:
            return False
    return Rule(_checker)


import aiohttp
import os

driver = get_driver()
tyf_file_group_id = driver.config.tyf_file_group_id
BOT_ID = str(driver.config.bot_id)

code_file = ['all_dnf_china_test_role_info.txt', 'all_dnf_china_exp2_role_info.txt', 'all_dnf_china_exp3_role_info.txt',
             'all_dnf_china_exp4_role_info.txt', 'all_dnf_china_exp5_role_info.txt', 'all_dnf_china_exp6_role_info.txt']

Inventory_Item_List = 'Inventory_Item_List.txt'

upload_test = on_notice(rule=check_tyf_file())

@upload_test.handle()
async def _(bot: Bot, event: Event, state: T_State):
    upload_file = event.file
    upload_file_name = upload_file.name
    upload_file_url = upload_file.url

    if upload_file_name in code_file:
        try:
            dirs = os.path.abspath(os.path.dirname(os.getcwd()))
            fig_dir = os.path.join(dirs, 'mysite', 'es', 'static', upload_file_name)
            await download_file(upload_file_url, fig_dir)
        except:
            await upload_test.send("自动上传失败，请手动上传角色表")
            return

        Region_id = code_file.index(upload_file_name) + 1

        if await update_server_time(Region_id):
            await upload_test.send(message=f'{Region_id}区角色表已更新')
        else:
            await upload_test.send(message=f'{Region_id}区角色表自动上传失败，请手动上传')
    elif upload_file_name == Inventory_Item_List:
        try:
            dirs = os.path.abspath(os.path.dirname(os.getcwd()))
            fig_dir = os.path.join(dirs, 'mysite', 'dnfbbs', upload_file_name)
            await download_file(upload_file_url, fig_dir)
            await upload_test.send(message=f'道具代码表已更新')
        except:
            await upload_test.send("自动上传失败，请手动上传道具代码表")


async def update_server_time(a):
    try:
        url = 'http://www.tianque.top/runtime/' + str(a - 1) + '/'
        async with aiohttp.ClientSession() as session:
            response = await session.get(url)
            content = await response.read()
        # print(content)
        if content == b'OK':
            return 1
        else:
            return 0
    except:
        return 0