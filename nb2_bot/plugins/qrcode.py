from nonebot import on_command,on_keyword
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nb2_bot.utils.Rt_api import get_qrcode
from nonebot.adapters.cqhttp.message import Message

__plugin_name__ = '二维码'
__plugin_usage__ = '发送 [二维码] [生成二维码] 来使用'


qrcode = on_command("qrcode", rule=to_me(), aliases={'二维码', '生成二维码', }, priority=5)

@qrcode.handle()
async def _(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    if args:
        state['text'] = args

@qrcode.got('text', prompt="你想生成什么内容的二维码呢？")
async def _(bot: Bot, event: Event, state: T_State):
    text = state['text']
    qrcode_send = await get_qrcode(text)
    await qrcode.send(Message('你的二维码是：' + qrcode_send), at_sender=True)