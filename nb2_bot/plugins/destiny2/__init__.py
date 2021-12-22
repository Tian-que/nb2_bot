from nonebot import on_command, permission, on_endswith
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.adapters.cqhttp.message import Message
from .weekly_report import *
from .today_report import *
from .data_source import *
from .update_today_report_to_heybox import *
from nb2_bot.utils import download_file

BOT_ID = str(driver.config.bot_id)

weekly_report = on_command("weekly_report", aliases={'周报', '老九', '试炼', }, priority=5)
get_perk = on_endswith("perk",priority=5)

@get_perk.handle()
async def _(bot: Bot, event: Event, state: T_State):
    msg = event.raw_message.split('perk')[0]
    if not len(msg):
        return
    try:
        fig_dir = await get_perks(msg)
        if fig_dir == None:
            return
        else:
            await get_perk.send(Message('[CQ:image,file=file:///' + fig_dir + ']'))
    except:
        await get_perk.send('出错了')




@weekly_report.handle()
async def _(bot: Bot, event: Event, state: T_State):
    target = event.raw_message
    if target == '周报':
        figurl, figname = await get_weekly_report()
    elif target == '老九':
        figurl, figname = await get_9_report()
    elif target == '试炼':
        figurl, figname = await get_osiris_report()
    else:
        return 0
    figname = figname + '.jpg'
    fig_dir = os.path.join(os.getcwd(), 'nb2_bot', 'data', 'destiny2', 'image', 'weekly_report', figname)
    if not os.path.exists(fig_dir):
        if not await download_file(figurl, fig_dir):
            await weekly_report.send('失败了')
            return
    await weekly_report.send(Message(f"[CQ:image,file=file:///{fig_dir}]"))

