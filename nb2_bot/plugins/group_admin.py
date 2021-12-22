from nonebot import on_request, on_command, get_driver, permission, on_notice
from nonebot.adapters.cqhttp import GroupRequestEvent, FriendRequestEvent, GroupMessageEvent, GroupIncreaseNoticeEvent
from nonebot.adapters import Bot, Event
from nonebot.matcher import Matcher
from nonebot.typing import T_State
from nb2_bot.utils.JsonIO import *
import time
from nonebot.message import run_preprocessor
from nonebot.exception import IgnoredException

import os

info = {}
fig_dir = os.path.join(os.getcwd(), 'nb2_bot', 'data', 'requests', 'friends.json')

driver = get_driver()
admin_group = driver.config.admin_group


@driver.on_bot_connect
async def get_member(bot: Bot):
    global info
    info = await readTo(fig_dir)


@run_preprocessor
async def only_prefix(matcher: Matcher, bot: Bot, event: Event, state: T_State):
    prefix:str = state.get('_prefix',{'raw_command':' '}).get('raw_command', ' ')
    if prefix not in ['tyf', '体验服', '日报']:
        return
    messageText = event.get_message().extract_plain_text()
    if messageText != prefix:
        raise IgnoredException("reason")
    pass


notice_event = on_notice()
request_event = on_request()


@notice_event.handle()
async def _(bot: Bot, event: GroupIncreaseNoticeEvent) -> None:
    if event.self_id == event.user_id:
        group_name = await bot.get_group_info(group_id=event.group_id)
        group_name = group_name['group_name']
        ret = f'已加入群: {group_name}({event.group_id})'
        await bot.send_group_msg(group_id=admin_group, message=ret)
    pass


@request_event.handle()
async def _(bot: Bot, event: GroupRequestEvent) -> None:
    nickname = await bot.get_stranger_info(user_id=event.user_id)
    nickname = nickname['nickname']
    group_name = await bot.get_group_info(group_id=event.group_id)
    group_name = group_name['group_name']
    if event.sub_type == 'add':
        ret = f'加群请求: {nickname}({event.user_id}) to 群: {group_name}({event.group_id}) 请求内容: {event.comment}'
    else:
        ret = f'加群邀请: {nickname}({event.user_id}) to 群: {group_name}({event.group_id})'
    await bot.send_group_msg(group_id=admin_group, message=ret)
    pass

request_query_group = on_command("request_query", aliases={'群验证',}, permission=permission.SUPERUSER)
@request_query_group.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    if event.group_id == admin_group:
        groupSystemMsg = await bot.get_group_system_msg()
        ret = ''
        if groupSystemMsg['join_requests']:
            ret += '\n'.join([f"{i['requester_nick']}({i['requester_uin']}) to {i['group_name']}({i['group_id']}) {i['message']}" for i in groupSystemMsg['join_requests'] if i['checked'] == False])
        if groupSystemMsg['invited_requests']:
            ret += '\n' + '\n'.join([f"{i['invitor_nick']}({i['invitor_uin']}) from {i['group_name']}({i['group_id']}) {i['message']}" for i in groupSystemMsg['invited_requests'] if i['checked'] == False])
        # ret = [f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(j['time']))} {j['nickname']}({i}) {j['comment']}" for i, j in info.items()]
        if ret == '\n':
            ret = '暂无待处理群验证信息'
        await request_query_group.send(ret.strip('\n'))


@request_event.handle()
async def _(bot: Bot, event: FriendRequestEvent) -> None:
    nickname = await bot.get_stranger_info(user_id = event.user_id)
    nickname = nickname['nickname']
    ret = f'好友请求: {nickname}({event.user_id}) 请求内容: {event.comment}'
    info[str(event.user_id)] = {
        'comment': event.comment,
        'nickname': nickname,
        'type': event.request_type,
        'time': event.time,
        'flag': event.flag
    }
    await writeTo(fig_dir, info)
    await bot.send_group_msg(group_id=admin_group, message=ret)


request_query = on_command("request_query", aliases={'好友验证', '好友'}, permission=permission.SUPERUSER)
@request_query.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    if event.group_id == admin_group:
        ret = [f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(j['time']))} {j['nickname']}({i}) {j['comment']}" for i, j in info.items()]
        if not ret:
            ret = ['暂无好友请求']
        await request_query.send('\n'.join(ret))

request_query_approve = on_command("request_query_approve", aliases={'通过好友',}, permission=permission.SUPERUSER)
@request_query_approve.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    if event.group_id == admin_group:
        args = event.message.extract_plain_text().strip()
        ret = '处理完毕'
        for i in args.split():
            if info.get(i):
                await bot.set_friend_add_request(flag=info.get(i)['flag'], approve=True)
                info.pop(i)
                ret += f'\n{i}\t已同意'
            else:
                ret += f'\n{i}\t未查询到请求'
        # ret = [f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(j['time']))} {i} {j['comment']}" for i, j in info.items()]
        await request_query_approve.send(ret)

request_query_approve_group = on_command("request_query_approve", aliases={'通过加群', }, permission=permission.SUPERUSER)
@request_query_approve_group.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    if event.group_id == admin_group:
        args = event.message.extract_plain_text().strip()
        groupSystemMsg = await bot.get_group_system_msg()
        ret = '处理完毕'
        for i in args.split():
            if groupSystemMsg['join_requests']:
                requestInfos = [j for j in groupSystemMsg['join_requests'] if int(i) == j['requester_uin'] and j['checked']== False]
                for requestInfo in requestInfos:
                    await bot.set_group_add_request(flag=str(requestInfo['request_id']),sub_type='add',approve=True)
                    ret += f'\n{i}\t已同意加群'
                if requestInfos:
                    continue
            if groupSystemMsg['invited_requests']:
                requestInfos = [j for j in groupSystemMsg['invited_requests'] if int(i) == j['group_id'] and j['checked']== False]
                for requestInfo in requestInfos:
                    await bot.set_group_add_request(flag=str(requestInfo['request_id']),sub_type='invite',approve=True)
                    ret += f'\n{i}\t已同意邀请'
                if requestInfos:
                    continue
            ret += f'\n{i}\t未查询到请求'
        # ret = [f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(j['time']))} {i} {j['comment']}" for i, j in info.items()]
        await request_query_approve_group.send(ret)
