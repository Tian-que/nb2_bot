from nonebot import on_command,on_keyword
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event

from .data_source import get_anime


__plugin_name__ = '识番'
__plugin_usage__ = ''


whatanime = on_command("whatanime", aliases={'whatanime', '识番', '識番', }, priority=5)

@whatanime.handle()
async def _(bot: Bot, event: Event, state: T_State):
    images = [seg.data.get('url') for seg in event.message if seg.type == "image"]
    if images:
        state['whatanime'] = images[0]


@whatanime.got('whatanime', prompt="图呢？GKD")
async def _(bot: Bot, event: Event, state: T_State):
    anime_data = state["whatanime"]
    anime_data_report = await get_anime(anime_data)
    if anime_data_report:
        await whatanime.send(anime_data_report, at_sender=True)
    else:
        await whatanime.send("[ERROR]Not found Anime")

@whatanime.args_parser
async def _(bot: Bot, event: Event, state: T_State):
    images = [seg.data.get('url') for seg in event.message if seg.type == "image"]
    if images:
        state['whatanime'] = images[0]
    else:
        await whatanime.finish('没图说个J*!', at_sender=True)