from nonebot import get_driver
from nonebot import require
scheduler = require('nonebot_plugin_apscheduler').scheduler
import aiohttp
from bs4 import BeautifulSoup

# __plugin_name__ = 'DNF论坛签到'
# __plugin_usage__ = '指令：[DNF论坛签到]'

driver = get_driver()
BOT_ID = str(driver.config.bot_id)
user_config = driver.config.user_config

# @on_command('qiandaoforjia', aliases=('DNF论坛签到'), only_to_me = False, permission = permission.SUPERUSER)
async def qiandaoforjia(user_id, user_cookie):
    bot = driver.bots[BOT_ID]
    try:
        # print(kwargs)
        ret = await gogogo(user_id, user_cookie)
        await bot.send_group_msg(group_id=694531998, message=ret)
        # await session.send(message=ret,at_sender=True)
    except:
        await bot.send_group_msg(group_id=694531998, message=user_id + ' 签到失败')
        # await session.send(message='签到失败',at_sender=True)


async def gogogo(user_id, user_cookie):
    url = 'https://dnf.gamebbs.qq.com/plugin.php?id=k_misign:sign'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
    cookie = user_cookie
    cookie_dict = {i.split("=")[0]: i.split("=")[-1] for i in cookie.split("; ")}

    async with aiohttp.ClientSession() as session:
        response = await session.get(url=url, headers=headers, cookies=cookie_dict)
        content = await response.read()

    soup = BeautifulSoup(content.decode(), 'lxml')
    all = soup.find_all('a', class_='logout')
    formhash = all[0]['href'].split('=')[-1]
    all = soup.find_all('a', class_='author')
    author = all[0]['href']

    url2 = f'https://dnf.gamebbs.qq.com/plugin.php?id=k_misign:sign&operation=qiandao&formhash={formhash}&format=empty'
    async with aiohttp.ClientSession() as session:
        response = await session.get(url=url2, headers=headers, cookies=cookie_dict)
        content = await response.read()
    soup = BeautifulSoup(content.decode(), 'lxml')
    all = soup.find_all('div', id="messagetext")
    c = all[0].contents[1].contents[0]

    url3 = f'https://dnf.gamebbs.qq.com/{author}'
    async with aiohttp.ClientSession() as session:
        response = await session.get(url=url3, headers=headers, cookies=cookie_dict)
        content = await response.read()
    soup = BeautifulSoup(content.decode(), 'lxml')
    all = soup.find_all('ul', class_="pf_l")
    jingyan = all[3].contents[3].contents[1]
    daibi = all[3].contents[14].contents[1]

    return f"{user_id} {c} 经验值{jingyan} 代币券{daibi}"

[scheduler.add_job(qiandaoforjia, 'cron', hour=i[0], minute=i[1],args = [i[2]['user_id'], i[2]['user_cookie']]) for i in user_config]
