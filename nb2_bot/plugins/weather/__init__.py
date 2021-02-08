from nonebot import on_command,on_keyword
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from jieba import posseg
from .data_source import get_weather_of_city

__plugin_name__ = '查询天气'
__plugin_usage__ = '发送 [天气] [今天天气怎么样？] [北京天气] 来查询天气'


weather = on_keyword(keywords={'天气', '天气预报', '查天气', }, priority=5)


@weather.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    # 对消息进行分词和词性标注
    words = posseg.lcut(args)

    city = None
    # 遍历 posseg.lcut 返回的列表
    for word in words:
        # 每个元素是一个 pair 对象，包含 word 和 flag 两个属性，分别表示词和词性
        if word.flag == 'ns':
            # ns 词性表示地名
            city = word.word
            break

    # 返回意图命令，前两个参数必填，分别表示置信度和意图命令名
    if city:
        state['city'] = city


@weather.got("city", prompt="你想查询哪个城市的天气呢？")
async def handle_city(bot: Bot, event: Event, state: T_State):
    city = state["city"]
    weather_report = await get_weather_of_city(city)
    await weather.finish(weather_report)

@weather.args_parser
async def _(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    # 对消息进行分词和词性标注
    words = posseg.lcut(args)

    city = None
    # 遍历 posseg.lcut 返回的列表
    for word in words:
        # 每个元素是一个 pair 对象，包含 word 和 flag 两个属性，分别表示词和词性
        if word.flag == 'ns':
            # ns 词性表示地名
            city = word.word
            break

    # 返回意图命令，前两个参数必填，分别表示置信度和意图命令名
    if city:
        state['city'] = city
    else:
        await weather.finish('啊，查不到')
