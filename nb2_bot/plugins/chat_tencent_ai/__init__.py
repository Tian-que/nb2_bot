from .tencent_ai import *
from nonebot import on_message
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.adapters.cqhttp.message import Message
from aiocqhttp.message import escape

import random

EXPR_DONT_UNDERSTAND = (
    '我现在还不太明白你在说什么呢，但没关系，以后的我会变得更强呢！',
    '我有点看不懂你的意思呀，可以跟我聊些简单的话题嘛',
    '其实我不太明白你的意思……',
    '抱歉哦，我现在的能力还不能够明白你在说什么，但我会加油的～',
    'WDNMD你这啥意思啊'
)

__plugin_name__ = '聊天机器人'
__plugin_usage__ = '接入Tencent AI，似乎不太聪明的亚子'

chating = on_message(rule=to_me(), priority=9)

@chating.handle()
async def _(bot: Bot, event: Event, state: T_State):


    # 获取可选参数，这里如果没有 message 参数，命令不会被中断，message 变量会是 None
    message = event.get_plaintext()

    # 通过封装的函数获取图灵机器人的回复
    # print(context_id(session.ctx, use_hash=True),context_id(session.ctx, mode='group', use_hash=True))
    reply = await chat(message, event.message_id)
    if reply:
        # 如果调用图灵机器人成功，得到了回复，则转义之后发送给用户
        # 转义会把消息中的某些特殊字符做转换，以避免 酷Q 将它们理解为 CQ 码
        await chating.send(escape(reply))
    else:
        # 如果调用失败，或者它返回的内容我们目前处理不了，发送无法获取图灵回复时的「表达」
        # 这里的 render_expression() 函数会将一个「表达」渲染成一个字符串消息
        await chating.send(random.choice(EXPR_DONT_UNDERSTAND))
