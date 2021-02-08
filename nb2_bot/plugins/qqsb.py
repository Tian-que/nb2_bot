# coding=utf-8
from nonebot import on_command, get_driver, on_keyword, permission
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.adapters.cqhttp.message import Message
from nb2_bot.utils.JsonIO import *
from nb2_bot.Rules import check_group_message


__plugin_name__ = '叫人帮忙'
__plugin_usage__ = '命令： 叫[谁][干什么]'

driver = get_driver()
BOT_ID = str(driver.config.bot_id)
group_list_upload = driver.config.group_list_upload


member = {}
fig_dir = os.path.join(os.getcwd(), 'nb2_bot', 'data', 'qqsb', 'qqsb.json')

@driver.on_startup
async def get_member():
    global member
    fig_dir = os.path.join(os.getcwd(), 'nb2_bot', 'data', 'qqsb', 'qqsb.json')
    member = await readTo(fig_dir)
    print('载入QQSB成功')


qqsb = on_keyword(keywords={'叫','说','喊','告诉'}, rule=check_group_message() & to_me(), priority=5)

@qqsb.handle()
async def _(bot: Bot, event: Event, state: T_State):
    stripped_msg = str(event.get_message()).strip()
    start = [i for i in ['叫','说','喊','告诉'] if stripped_msg.startswith(i)]
    if not start:
        return
    stripped_msg = stripped_msg[len(start[0]):]
    a = [k for k,v in member.items() if k in stripped_msg]
    if a:
        for k in a:
            stripped_msg = stripped_msg.replace(k,f"[CQ:at,qq={str(member[k])}]")
            # print(stripped_msg)
        stripped_arg = stripped_msg

        if '天阙' in a:
            stripped_arg = f"[CQ:at,qq={event.get_user_id()}] 你是猪"
        # if '七夕' not in stripped_msg or a[0] == '天阙':
        #     current_arg = stripped_msg
        # print(current_arg)
        # else:
        #     current_arg =stripped_msg + '孤寡\t孤寡\t孤寡\t孤寡\t孤寡\t孤寡'
        await qqsb.send(Message(stripped_arg))

add_member = on_command("add_member", aliases={'添加转义', }, priority=5, permission=permission.SUPERUSER)

@add_member.handle()
async def _(bot: Bot, event: Event, state: T_State):
    global member
    stripped_arg = str(event.get_message()).strip()
    member_k = [k for k, v in member.items()]

    try:
        stripped_arg = stripped_arg.split('\n')
        for arg in stripped_arg:
            arg = arg.split(' ')
            if not arg[1].isdigit():
                await add_member.send('数据格式错误，请重新调用命令')
                return
            if arg[0] in member_k:
                await add_member.send('已经有这给人了哦:' + arg[0]  + ' ' + str(arg[1]))
                return
            member[arg[0]] = int(arg[1])

        await writeTo(fig_dir,member)
        await add_member.send('添加成功')
    except:
        await add_member.send('数据格式错误，请重新调用命令')

dec_member = on_command("dec_member", aliases={'删除转义', }, priority=5, permission=permission.SUPERUSER)

@dec_member.handle()
async def _(bot: Bot, event: Event, state: T_State):
    global member
    stripped_arg = str(event.get_message()).strip()
    member_k = [k for k, v in member.items()]

    try:
        stripped_arg = stripped_arg.split('\n')
        for arg in stripped_arg:
            if arg in member_k:
                member.pop(arg)
                await dec_member.send('删除成功' + arg)
                await writeTo(fig_dir, member)
                return
            else:
                await dec_member.send('没有这个转义哦')
    except:
        await dec_member.send('数据格式错误，请重新调用命令')
