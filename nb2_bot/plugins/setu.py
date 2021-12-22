from nonebot import on_command, get_driver
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.adapters.cqhttp.message import Message, MessageSegment
import asyncio
import ujson,requests
import aiohttp
import time,os
import random
from nonebot.rule import Rule

__plugin_name__ = ''
__plugin_usage__ = ''

driver = get_driver()

# URL = 'https://api.lolicon.app/setu/'
# API_KEY = driver.config.setu_api_key
#
# SETU_REPLY = """Title: {title}
# Pid: {pid}
# {setu}
# """

# async def request_api_params(url, params):
#     response = requests.get(url, params = params,timeout = 20)
#     html = response.text
#     return html

# async def download_img(url):
#     async with aiohttp.ClientSession() as session:
#         response = await session.get(url)
#         content = await response.read()
#     figName = time.strftime("%Y_%m_%d%H_%M_%S", time.localtime()) + '-' + url.split('/')[-1]
#     fig_dir = os.path.join(os.getcwd(), 'nb2_bot', 'data','setu','images',figName)
#     with open(fig_dir, 'wb') as f:
#         f.write(content)
#     return '[CQ:image,file=file:///' + fig_dir + ']'

def check_setu_ban_group_id() -> Rule:
    async def _checker(bot: Bot, event: Event, state: T_State) -> bool:
        try:
            if event.group_id in [978717771]:
                return False
            else:
                return True
        except:
            return True

    return Rule(_checker)


async def get_img():
    img = os.listdir(os.path.join(os.getcwd(), 'nb2_bot', 'data','setu','images'))
    fig_dirs = [os.path.join(os.getcwd(), 'nb2_bot', 'data','setu','images' + '\\' + random.choice(img)) for _ in range(3)]

    return [MessageSegment.image(file='file:///' + i) for i in fig_dirs]


setu_bot = on_command("setu_bot",rule=check_setu_ban_group_id(), aliases={'色图', '涩图', '来张涩图','来张色图','来份色图', }, priority=5)

@setu_bot.handle()
async def _(bot: Bot, event: Event, state: T_State):
    fig_info = await get_img()
    for i in range(3):
        try:
            msg_id = await setu_bot.send(message=Message(fig_info[i]))
            # print(msg_id)
            await asyncio.sleep(1)
            await bot.delete_msg(message_id=msg_id['message_id'])
            return
        except:
            continue
    await setu_bot.send(message=Message("连抽三张全风控，建议跳楼"))

    # if str(event.get_message()).strip() == 'GKD':
    #     values = {
    #         "apikey": API_KEY,
    #         "r18": "1",
    #         "num": "1"
    #     }
    # else:
    #     values = {
    #         "apikey": API_KEY,
    #         "r18": "0",
    #         "num": "1"
    #     }
    # try:
    #     dc = ujson.loads(await request_api_params(URL, values))
    #     title = dc["data"][0]["title"]
    #     pid = dc["data"][0]["pid"]
    #     setu = dc["data"][0]["url"]  # b64.b64_str_img_url(dc["data"][0]["url"])
    # except:
    #     await setu_bot.send('失败了')
    #     return
    # await setu_bot.send('别急！我拿到链接了，下载下来就给你！')
    # try:
    #     setu2 = await download_img(setu)
    #     await setu_bot.send(Message(
    #         SETU_REPLY.format(
    #             title=title,
    #             pid=pid,
    #             setu=setu2
    #         )), at_sender=True)
    # except:
    #     await setu_bot.send('下载失败了')

