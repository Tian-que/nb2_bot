import aiohttp
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.adapters.cqhttp.message import Message
import time


scoregg = on_command("scoregg", aliases={'夺冠了', '赛程', 'LPL', 'LOL', 'lpl', 'lol'}, priority=5)
LPL_Team = ['RNG', 'LNG', 'FPX', 'EDG']


@scoregg.handle()
async def _(bot: Bot, event: Event, state: T_State):
    if str(event.get_message()) == '吗':
        ret = await bet_single_list(1)
    else:
        ret = await bet_single_list()
    await scoregg.send(Message(ret))

async def bet_single_list(d = 0):
    url = 'https://www.scoregg.com/services/api_url.php'
    headers = {
        'Origin': 'https://www.scoregg.com',
        'Referer': 'https://www.scoregg.com/match_pc?tournamentID=207',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0',
    }

    data = {
        "api_path": "/services/bet/bet_single_list.php",
        "method": "post",
        "platform": "web",
        "api_version": "9.9.9",
        "language_id": "1",
        "tournament_id": "207",
        "type": "10",
    }
    async with aiohttp.ClientSession() as session:
        response = await session.post(url=url, headers = headers, data = data)
        data = await response.json(content_type='text/html')

    match_list = data['data']['list']
    if not d:
        all_match = [f"{time.strftime('%m-%d %H:%M', time.localtime(int(i['match_start_time'])))}\t{i['match_team_a']:3s} VS {i['match_team_b']:3s}" for i in match_list]
    else:
        all_match = [
            f"{time.strftime('%m-%d %H:%M', time.localtime(int(i['match_start_time'])))}\t{i['match_team_a']:3s} VS {i['match_team_b']:3s}"
            for i in match_list if i['match_team_a'] in LPL_Team or i['match_team_b'] in LPL_Team]
    ret = '近期赛程如下\n' + '\n'.join(all_match[:10])
    return ret