from nonebot import on_command, permission, on_endswith
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from .data_source import get_image_data

__plugin_name__ = '识图'
__plugin_usage__ = ''

find_image = on_command('find_image', aliases={'image', '搜图', '识图', }, priority=5)

@find_image.handle()
async def _(bot: Bot, event: Event, state: T_State):
    images = [seg.data.get('url') for seg in event.message if seg.type == "image"]
    if images:
        state['image'] = images[0]


@find_image.got("image", prompt="图呢？GKD")
async def _(bot: Bot, event: Event, state: T_State):
    image_data = state["image"]
    image_data_report = await get_image_data(image_data, 'b0567d13f7b46b9f832c1e46a58faf43515ec3a5')
    if image_data_report:
        await find_image.finish(image_data_report, at_sender=True)
    else:
        await find_image.finish("[ERROR]Not found imageInfo", at_sender=True)
    pass


@find_image.args_parser
async def _(bot: Bot, event: Event, state: T_State):
    images = [seg.data.get('url') for seg in event.message if seg.type == "image"]
    if images:
        state['image'] = images[0]
    else:
        await find_image.finish('没图说个J*!', at_sender=True)