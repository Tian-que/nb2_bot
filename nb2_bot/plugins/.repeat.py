from nonebot import on_command, get_driver, on_message
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot import require

scheduler = require('nonebot_plugin_apscheduler').scheduler
from nonebot.rule import Rule

import time

driver = get_driver()
BOT_ID = str(driver.config.bot_id)
src_group_id = driver.config.group_list_upload
des_group_id = driver.config.group_list_upload


def check_repeat() -> Rule:
    async def _checker(bot: Bot, event: Event, state: T_State) -> bool:
        if event.get_type() == 'message' and event.message_type == 'group' and event.group_id == src_group_id:
            return True
        else:
            return False

    return Rule(_checker)


repeat = on_message(priority=5)


@repeat.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    try:

        stripped_arg = f'群[{event.group_id}]内{event.sender.nickname}[{event.get_user_id()}]：' + str(event.get_message()).strip()
        # event.group_id
        # event.get_user_id()

        bot = driver.bots[BOT_ID]
        await bot.send_group_msg(group_id=des_group_id, message=stripped_arg)
    except:
        await repeat.send(message='服务不可用', at_sender=True)
