from nonebot import on_request, on_command
from nonebot.adapters.cqhttp import GroupRequestEvent
from nonebot.adapters import Bot, Event
from nonebot.typing import T_State


import os
from os import listdir
import pandas as pd

__plugin_name__ = '自动批人名单管理[超级管理员功能]'
__plugin_usage__ = '命令： [成员名单] [名单管理] [成员名单管理]'

# 获取监听群列表
group_list_dir = listdir(os.path.join(os.getcwd(), 'nb2_bot', 'data', 'group_admin', ))
group_list = [int(i.strip(".txt")) for i in group_list_dir]

request_group_event = on_request()

@request_group_event.handle()
async def _(bot, event: GroupRequestEvent) -> None:
    if event.group_id in group_list:
        if await check_permission(event.group_id, event.user_id):
            await event.approve(bot)
            return
        await event.reject(bot, reason='此QQ无权入群')
    pass

async def check_permission(group_num, qq):
    df = pd.read_csv(os.path.join(os.getcwd(), 'nb2_bot', 'data', 'group_admin', str(group_num) + '.txt'), sep='\t', header=0)
    data = df.loc[df.iloc[:,0] == qq]
    return len(data)


# test = on_command("test", priority=5)
#
# @test.handle()
# async def _(bot: Bot, event: Event, state: T_State):
#     join_requests = await bot.get_group_system_msg()
#     for join_request in join_requests['join_requests']:
#         # print('\n'.join([f"{j}: {k}" for j,k in join_request.items()]))
#         if join_request['actor'] == 0:
#             print(join_request)
#             await bot.set_group_add_request(flag=str(join_request['request_id']), sub_type='add', approve = True)