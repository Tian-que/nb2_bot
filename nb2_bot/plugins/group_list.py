# coding=utf-8
from nonebot import on_command, permission, get_driver
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nb2_bot.utils import *
import time

__plugin_name__ = '导出群成员[超级管理员功能]'
__plugin_usage__ = '命令： [群] [群成员] [导出群成员]'


driver = get_driver()
BOT_ID = str(driver.config.bot_id)
group_list_upload = driver.config.group_list_upload

group_list = on_command("group_list", aliases={'群', '群成员', '导出群成员', }, priority=5, permission=permission.SUPERUSER)

@group_list.handle()
async def _(bot: Bot, event: Event, state: T_State):
    info = await bot.get_group_list()
    state['group_list'] = [str(item['group_id']) for item in info]
    state['group_info'] = '\n'.join([f"{item['group_id']} {item['group_name']}" for item in info])

    args = str(event.get_message()).strip()
    if args in state['group_list']:
        state['group_number'] = args



@group_list.got("group_number", prompt="你想导出哪个群的成员呢？\n{group_info}")
async def _(bot: Bot, event: Event, state: T_State):
    group_number = state['group_number']
    info2 = await bot.get_group_member_list(group_id=int(group_number))
    data = 'QQ 群名片\n' + '\n'.join([f"{item['user_id']} {item['card']}" for item in info2])

    figname = group_number + '_' + time.strftime("%Y_%m_%d%H_%M_%S", time.localtime()) + '.txt'
    fig_dir = os.path.join(os.getcwd(), 'nb2_bot', 'data', 'group_list', figname)
    if await write_file(data, fig_dir):
        await bot.upload_group_file(group_id = group_list_upload, file = fig_dir, name = figname)
    await group_list.send('搞定，你的名单传上去了', at_sender=True)
    pass


@group_list.args_parser
async def _(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    group_lst = state['group_list']

    if args in group_lst:
        state['group_number'] = args
    else:
        await group_list.finish('没有这个群，请重新发送命令', at_sender=True)

