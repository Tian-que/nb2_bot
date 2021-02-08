from nonebot import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nb2_bot.utils import paste


__plugin_name__ = '贴代码'
__plugin_usage__ = '将代码转换为url 发送 [贴代码] [粘贴代码] [剪切板] 来使用'

pastebin = on_command("pastebin", rule=to_me(), aliases={'贴代码', '粘贴代码', '剪切板', '粘贴板', '粘贴'}, priority=5)

@pastebin.handle()
async def _(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    if args:
        state['code'] = args

@pastebin.got('code', prompt="你想粘贴什么呢？")
async def _(bot: Bot, event: Event, state: T_State):
    code = state['code']
    paste_send = await paste(code)
    if not paste_send:
        paste_send = '服务暂不可用'
    await pastebin.finish('搞定，你的东西都在这儿：' + paste_send, at_sender=True)
