from nonebot import on_notice, get_driver
from nonebot.adapters.cqhttp import GroupRecallNoticeEvent
from nonebot.adapters import Bot, Event
from nonebot.typing import T_State
from nonebot.rule import Rule
from aiocqhttp.message import escape

driver = get_driver()
admin_group = driver.config.admin_group
BOT_ID = str(driver.config.bot_id)


def check_recall() -> Rule:
    async def _checker(bot: Bot, event: Event, state: T_State) -> bool:
        if event.get_event_name() == 'notice.group_recall' and event.get_user_id()!= BOT_ID:
            return True
        return False
    return Rule(_checker)


anti_recall = on_notice(rule=check_recall())

@anti_recall.handle()
async def _(bot: Bot, event: GroupRecallNoticeEvent):
    d = await bot.get_msg(message_id = event.message_id)
    ret = f"群<{event.group_id}>内<{d['sender']['nickname']}:{d['sender']['user_id']}>撤回了消息：{d['raw_message']}"
    await bot.send_group_msg(group_id=admin_group,message=ret)
    pass