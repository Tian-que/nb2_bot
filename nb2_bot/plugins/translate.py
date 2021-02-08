from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nb2_bot.utils.Rt_api import get_translation

__plugin_name__ = '中英互译'
__plugin_usage__ = '发送 [翻译] [翻译一下] + 要翻译的内容 来使用'

translate = on_command("translate", aliases={'翻译', '翻译一下', }, priority=5)

@translate.handle()
async def _(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    if args:
        state['text'] = args


@translate.got('text', prompt="你要翻译什么呢？")
async def _(bot: Bot, event: Event, state: T_State):
    text = state['text']
    translate_send = await get_translation(text)
    await translate.send(translate_send, at_sender=True)
