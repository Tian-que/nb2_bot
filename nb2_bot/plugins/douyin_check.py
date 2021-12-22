import aiohttp
from nonebot import on_command, permission, get_driver
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot import require
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import asyncio
import time


scheduler = require('nonebot_plugin_apscheduler').scheduler

__plugin_name__ = ''
__plugin_usage__ = ''

now_state = None
driver = get_driver()
BOT_ID = str(driver.config.bot_id)

# 创建chrome浏览器驱动，无头模式
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument("--start-maximized")
# 不加载图片
prefs = {'profile.default_content_setting_values': {'images': 2,}}
chrome_options.add_experimental_option('prefs', prefs)


dy_fsf = on_command("dy_fsf", aliases={'testtest', }, priority=5, permission=permission.SUPERUSER)
@dy_fsf.handle()
async def _(bot: Bot, event: Event, state: T_State):
    try:
        ret = await is_check()
        await dy_fsf.send(message=str('\n'.join((' '.join([j for j in i]) for i in ret[:15]))))
    except:
        await dy_fsf.send(message='服务不可用', at_sender=True)


async def is_check():
    driver = webdriver.Chrome(r"C:\Program Files\Google\Chrome\Application\chromedriver.exe",
                              chrome_options=chrome_options)
    # 加载界面
    driver.get('https://live.douyin.com/category/1_569_1_1102')
    await asyncio.sleep(0.5)
    # 获取页面初始高度
    js = "return action=document.body.scrollHeight"
    height = driver.execute_script(js)

    # 将滚动条调整至页面底部
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    await asyncio.sleep(0.5)

    # 定义初始时间戳（秒）
    t1 = int(time.time())

    # 定义循环标识，用于终止while循环
    status = True

    # 重试次数
    num = 0

    while status:
        # 获取当前时间戳（秒）
        t2 = int(time.time())
        # 判断时间初始时间戳和当前时间戳相差是否大于30秒，小于30秒则下拉滚动条
        if t2 - t1 < 3:
            new_height = driver.execute_script(js)
            if new_height > height:
                await asyncio.sleep(1)
                driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
                # 重置初始页面高度
                height = new_height
                # 重置初始时间戳，重新计时
                t1 = int(time.time())
        elif num < 3:  # 当超过30秒页面高度仍然没有更新时，进入重试逻辑，重试3次，每次等待30秒
            await asyncio.sleep(1)
            num = num + 1
        else:  # 超时并超过重试次数，程序结束跳出循环，并认为页面已经加载完毕！
            # print("滚动条已经处于页面最下方！")
            status = False
            # 滚动条调整至页面顶部
            # driver.execute_script('window.scrollTo(0, 0)')
            break
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    datas = soup.find_all('a', rel="opener")
    ret = []
    for i in datas:
        info = [j.text for j in i.contents][::-1] + [i['href']]
        ret.append(info)

    driver.close()
    return ret

