from nb2_bot.utils.HeyBox import *
import aiohttp
from nb2_bot.utils.JsonIO import *
from nonebot import on_command, get_driver
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.adapters.cqhttp.message import Message
from nonebot.rule import Rule
from nonebot import require
import time

scheduler = require('nonebot_plugin_apscheduler').scheduler

def check_d2_admin_group() -> Rule:
    async def _checker(bot: Bot, event: Event, state: T_State) -> bool:
        if event.group_id == d2_admin_group:
            return True
        else:
            return False
    return Rule(_checker)

driver = get_driver()
BOT_ID = str(driver.config.bot_id)
d2_admin_group = driver.config.d2_file_group_id

today_report_creat = on_command("today_report_creat", rule=check_d2_admin_group(), aliases={'日报自动发帖', }, priority=5)
today_report_recreat = on_command("today_report_recreat", rule=check_d2_admin_group(), aliases={'日报重置帖子', }, priority=5)
today_report_edit = on_command("today_report_edit", rule=check_d2_admin_group(), aliases={'日报要点修改', }, priority=5)

@today_report_creat.handle()
async def _(bot: Bot, event: Event, state: T_State):
    try:
        ret = await creat_article()
    except:
        ret = '发送失败'
    await today_report_creat.send(Message(ret))

@today_report_recreat.handle()
async def _(bot: Bot, event: Event, state: T_State):
    try:
        ret = await recreat_article()
    except:
        ret = '重置失败'
    await today_report_recreat.send(Message(ret))

async def recreat_article():
    url = 'http://www.tianque.top/d2api/today/'
    async with aiohttp.ClientSession() as session:
        response = await session.get(url=url)
        img_data = await response.json()

    fig_dir = os.path.join(os.getcwd(), 'nb2_bot', 'data', 'destiny2', 'image', 'today_report', 'today_report.json')
    cache = await readTo(fig_dir)
    today = img_data['today']
    if cache == 0 or today != cache.get('today'):
        return "今天还未发日报，请输入 日报自动发帖 以发送日报"

    url = 'http://www.tianque.top/d2api/tjson/'
    async with aiohttp.ClientSession() as session:
        response = await session.get(url=url)
        today_data = await response.json()
    if today_data.get('error'):
        raise
    tittle = f'《命运2》 日报 - {today_data["season_date_info"]["today"]}'
    points = []
    points.append(f"1320遗失掉落{today_data['Lost']['1320']['掉落部位']}，1350遗失掉落{today_data['Lost']['1350']['掉落部位']}")
    mod = []
    for item in today_data['Vendor1'][:2]:
        if item['itemTypeDisplayName'] in ['充斥光能模组','战争思维电池模组']:
            mod.append(f"{item['name']}({item['itemTypeDisplayName']})")
    if mod:
        points.append(f"枪酱做人售卖{'+'.join(mod)}")
    wg_cost = today_data['Vendor2'][0]['costs'][0][0]
    if wg_cost == '微相数据格':
        wg_cost = '数据格'
    if wg_cost == '传说碎片':
        points.append(f"蛛王可传说碎片直换微光（不推荐）")
    elif wg_cost in [i['name'] for i in today_data['Vendor2'][1:] if i['costs'][0][0] == '传说碎片']:
        points.append(f"蛛王可换微光（{wg_cost}）")
    text = await build_text(points = points, img_url = img_data['img_url'], img_height= img_data['height'])
    link_id = cache['link_id']
    h.article_edit(tittle=tittle, text=text, link_id=link_id)
    data = {
        'today': today,
        'tittle': tittle,
        'points': points,
        'img_data': img_data,
        'link_id': link_id,
        'url': f"https://www.xiaoheihe.cn/community/65410/list/{link_id}"
    }
    await writeTo(fig_dir,data)
    return  f"日报重置帖子成功: \n" \
            f"标题: {tittle}\n" \
            f"URL: https://www.xiaoheihe.cn/community/65410/list/{link_id}"

async def creat_article():
    url = 'http://www.tianque.top/d2api/today/'
    async with aiohttp.ClientSession() as session:
        response = await session.get(url=url)
        img_data = await response.json()
    if img_data.get('error'):
        raise
    fig_dir = os.path.join(os.getcwd(), 'nb2_bot', 'data', 'destiny2', 'image', 'today_report', 'today_report.json')
    cache = await readTo(fig_dir)
    today = img_data['today']
    if time.strftime('%Y-%m-%d', time.localtime(time.time() - 3600)) != today:
        raise
    if cache != 0 and today == cache.get('today'):
        return f"今天日报已经发了哦: \n" \
               f"标题: {cache['tittle']}\n" \
               f"URL: {cache.get('url')}"
        pass

    url = 'http://www.tianque.top/d2api/tjson/'
    async with aiohttp.ClientSession() as session:
        response = await session.get(url=url)
        today_data = await response.json()
    if today_data.get('error'):
        raise
    tittle = f'《命运2》 日报 - {today_data["season_date_info"]["today"]}'
    points = []

    points.append(f"1320遗失掉落{today_data['Lost']['1320']['掉落部位']}，1350遗失掉落{today_data['Lost']['1350']['掉落部位']}")
    mod = []
    for item in today_data['Vendor1'][:2]:
        if item['itemTypeDisplayName'] in ['充斥光能模组','战争思维电池模组']:
            mod.append(f"{item['name']}({item['itemTypeDisplayName']})")
    if mod:
        points.append(f"枪酱做人售卖{'+'.join(mod)}")
    wg_cost = today_data['Vendor2'][0]['costs'][0][0]
    if wg_cost == '微相数据格':
        wg_cost = '数据格'
    if wg_cost == '传说碎片':
        points.append(f"蛛王可传说碎片直换微光（不推荐）")
    elif wg_cost in [i['name'] for i in today_data['Vendor2'][1:] if i['costs'][0][0] == '传说碎片']:
        points.append(f"蛛王可换微光（{wg_cost}）")
    text = await build_text(points = points, img_url = img_data['img_url'], img_height= img_data['height'])
    link_id = h.article_new(tittle=tittle, text=text)
    data = {
        'today': today,
        'tittle': tittle,
        'points': points,
        'img_data': img_data,
        'link_id': link_id,
        'url': f"https://www.xiaoheihe.cn/community/65410/list/{link_id}"
    }

    await writeTo(fig_dir,data)
    return  f"日报自动发帖成功: \n" \
            f"标题: {tittle}\n" \
            f"URL: https://www.xiaoheihe.cn/community/65410/list/{link_id}"

@today_report_edit.handle()
async def _(bot: Bot, event: Event, state: T_State):
    url = 'http://www.tianque.top/d2api/today/'
    async with aiohttp.ClientSession() as session:
        response = await session.get(url=url)
        img_data = await response.json()

    fig_dir = os.path.join(os.getcwd(), 'nb2_bot', 'data', 'destiny2', 'image', 'today_report', 'today_report.json')
    cache = await readTo(fig_dir)
    today = img_data['today']
    if cache == 0 or today != cache.get('today'):
        ret = "今天还未发日报，请输入 日报自动发帖 以发送日报"
        await today_report_edit.finish(Message(ret))

    state['tittle'] = cache['tittle']
    state['link_id'] = cache['link_id']
    state['url'] = cache['url']
    state['points'] = '\n'.join(cache['points'])
    state['img_data'] = cache['img_data']
    state['cache'] = cache

    args = str(event.get_message()).strip()
    if args:
        state['new_points'] = args.split()

@today_report_edit.got("new_points", prompt="标题: {tittle}\nURL: {url}\n当前要点: \n{points}\n\n请输入修改后要点")
async def _(bot: Bot, event: Event, state: T_State):
    points = state['new_points']
    img_data = state['img_data']

    text = await build_text(points=points, img_url=img_data['img_url'], img_height=img_data['height'])
    h.article_edit(tittle=state['tittle'],text=text,link_id=state['link_id'])
    point = '\n'.join(points)
    fig_dir = os.path.join(os.getcwd(), 'nb2_bot', 'data', 'destiny2', 'image', 'today_report', 'today_report.json')
    data = {
        'today': state['cache']['today'],
        'tittle': state['cache']['tittle'],
        'points': points,
        'img_data': img_data,
        'link_id': state['cache']['link_id'],
        'url': state['cache']['url']
    }
    await writeTo(fig_dir,data)
    ret = f"日报要点修改成功: \n" \
            f"tittle: {state['tittle']}\n" \
            f"URL: {state['url']}\n" \
            f"要点: \n{point}"
    await today_report_edit.send(Message(ret))

#
@today_report_edit.args_parser
async def _(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    if args:
        state['new_points'] = args.split()
    else:
        await today_report_edit.finish('参数错误，请重新调用命令', at_sender=True)

async def build_text(points, img_url, img_height):
    return [{"type":"html","text":f"<h2><b>今日的命运2:</b></h2><ul>{''.join([f'<li><b>{i}</b></li>' for i in points])}</ul><p><img class=\"lazy\" data-width=\"1063\" data-height=\"{img_height}\" data-original=\"{img_url}\"></p><p>日报于每日 1:03 自动投稿，如命运2更新日等情况会在API维护结束后投稿。</p><p>同时欢迎各位来对日报提建议：<a href=\"https://api.xiaoheihe.cn/v3/bbs/app/api/web/share?link_id=76390615\" target=\"_blank\">日报反馈贴</a></p><p><br></p><p>版权声明:</p><blockquote><p>版权声明</p><p>在本网站发表的文章(包括转帖)，版权归原作者所有</p><p>在征得作者同意的情况下，日报允许非盈利性引用，并请注明出处：“作者：kamuxiy、wenmumu、天阙”字样，以尊重作者的劳动成果</p><p>本网站的所有作品会由作者及时更新，欢迎大家阅读后发表评论，以利作品的完善</p></blockquote><p><br></p><p>&nbsp;<a href=\"heybox://open_subject\" target=\"_blank\">#命运2日报#</a>  </p>"},{"type":"img","url":img_url,"width":"1063","height":str(img_height)}]


async def auto_post():
    bot = driver.bots[BOT_ID]
    try:
        ret = await creat_article()
        await bot.send_group_msg(group_id=d2_admin_group, message=f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}\n' + ret)
    except:
        await bot.send_group_msg(group_id=d2_admin_group, message=f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}\n日报自动发送失败 将于一小时后重试')
        scheduler.add_job(auto_post, 'date', run_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() + 3600)))




scheduler.add_job(auto_post, 'cron', hour=1, minute=3)