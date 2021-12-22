from nonebot import on_request, on_command, get_driver, permission, on_message
from nonebot.adapters.cqhttp import GroupRequestEvent, FriendRequestEvent, GroupMessageEvent
from nonebot.adapters import Bot, Event
from nonebot.matcher import Matcher
from nonebot.typing import T_State
from nb2_bot.utils.JsonIO import *
import time
from nonebot.message import run_preprocessor
from nonebot.exception import IgnoredException

message_event = on_message()


@message_event.handle()
async def _(bot: Bot, event: GroupMessageEvent) -> None:
    forwardId = [seg.data.get('id') for seg in event.message if seg.type == 'forward']
    forwardData = await bot.get_forward_msg(message_id = forwardId[0])
    a = 0