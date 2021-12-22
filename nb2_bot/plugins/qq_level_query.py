from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event

import asyncio



qq_level_query = on_command("qq_level_query", aliases={'查询等级', }, priority=5)

@qq_level_query.handle()
async def _(bot: Bot, event: Event, state: T_State):
    a = []
    args = str(event.get_message()).strip()

    for qq_num in args.split():
        try:
            await asyncio.sleep(1)
            data = await bot.get_stranger_info(user_id=int(qq_num))
            if data['level'] == 0:
                data['level'] = 'error'
            a.append(data)
        except:
            a.append({'user_id':int(qq_num),'level':'error'})
            pass
    await qq_level_query.send('\n'.join([f"{i['user_id']}\t{i['level']}" for i in a]))