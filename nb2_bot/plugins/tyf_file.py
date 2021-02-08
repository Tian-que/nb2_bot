from nonebot import on_command, get_driver
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot import require
scheduler = require('nonebot_plugin_apscheduler').scheduler


import time
import requests
import asyncio

driver = get_driver()
TYF_STATE_PUSH_LIST = driver.config.tyf_state_push_list
BOT_ID = str(driver.config.bot_id)

Region_file_url = {
    "天界": {
        "tcls": "http://down-update.qq.com/dnf/autopatch/dnf_exp/dnf.exp12.full.tct/tcls.lst",
        "auto": "http://down-update.qq.com/dnf/autopatch/dnf_exp/dnf.exp12.full.tct/auto.lst"
    },
    "格兰": {
        "tcls": "http://down-update.qq.com/dnf/autopatch/dnf_exp/dnf.exp34.full.tct/tcls.lst",
        "auto": "http://down-update.qq.com/dnf/autopatch/dnf_exp/dnf.exp34.full.tct/auto.lst",
    },
    "魔界": {
        "tcls": "http://down-update.qq.com/dnf/autopatch/dnf_exp/dnf.exp56.full.tct/tcls.lst",
        "auto": "http://down-update.qq.com/dnf/autopatch/dnf_exp/dnf.exp56.full.tct/auto.lst"
    }
}
now_state = []
# now_state = ['天界:9b6151e9df1d5c214b1557bbec270f80f5db9e4cc3d3b36c96ae9499326616c6c', '格兰:a66529bc179a2256c4a517d325e8379642bf5ba8b6714e46fb77d7b7dc4fa3cf', '魔界:a37db78c72bc4e17257ea5e6e9d0606c9ed8212566f3b86844ae47999b2d4e1b']


tyf_file_md5 = on_command("tyf_file_md5", aliases={'体验服2',}, priority=5)

@tyf_file_md5.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    try:
        await tyf_file_md5.send(
            message=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n' + '\n'.join(i for i in now_state))
    except:
        await tyf_file_md5.send(message='服务不可用', at_sender=True)

async def is_open(name, **kwargs):
    ret = name + ':'
    for k, v in kwargs.items():
        ret += requests.head(v).headers['X-COS-META-MD5']
    return ret

async def state_notice():
    global now_state
    ret = [await is_open(name=k, **v) for k, v in Region_file_url.items()]
    # new_state = [j for i in ret for j in i]
    new_state = ret
    if now_state:
        if new_state != now_state:
            mes = '[文件更新]' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            for i in range(len(now_state)):
                if now_state[i] != new_state[i]:
                    mes += f"\n{new_state[i].split(':')[0]}服务器文件有更新"
            # print(mes)
            for group in TYF_STATE_PUSH_LIST:
                try:
                    bot = driver.bots[BOT_ID]
                    await bot.send_group_msg(group_id=group, message=mes)
                    await asyncio.sleep(1)
                except:
                    pass
    now_state = new_state

scheduler.add_job(state_notice, 'interval', seconds=10)