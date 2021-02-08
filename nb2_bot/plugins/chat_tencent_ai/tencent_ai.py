import random
import string
import time
from hashlib import md5
from typing import Dict, Optional, Any
from urllib.parse import urlencode
from nonebot import get_driver

import httpx


STT_API_URL = 'https://api.ai.qq.com/fcgi-bin/aai/aai_asr'
TTS_API_URL = 'https://api.ai.qq.com/fcgi-bin/aai/aai_tts'
CHAT_API_URL = 'https://api.ai.qq.com/fcgi-bin/nlp/nlp_textchat'

driver = get_driver()


def get_app_id() -> str:
    return driver.config.tencent_ai_app_id


def get_app_key() -> str:
    return driver.config.tencent_ai_app_key


def calc_sign(params: Dict[str, str]) -> None:
    query = urlencode(dict(sorted((x, y) for x, y in params.items() if y)))
    query += f'&app_key={get_app_key()}'
    params['sign'] = md5(query.encode()).hexdigest().upper()


async def do_post_request(url: str,
                          params: Dict[str, str]) -> Optional[Dict[str, Any]]:
    if not params.get('sign'):
        calc_sign(params)


    # print(params)
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, data=params, timeout = 3)
    payload = resp.json()
    # print(payload)
    if payload.get('ret') == 0:
        return payload['data']
    return None


def gen_base_params() -> Dict[str, str]:
    letters_digits = string.ascii_letters + string.digits
    return {
        'app_id': get_app_id(),
        'time_stamp': str(int(time.time())),
        'nonce_str': ''.join(random.choice(letters_digits) for _ in range(10)),
        'sign': ''
    }


async def stt(speech_base64: str) -> Optional[str]:
    """
    语音转文本(语音识别).

    Args:
        speech_base64: 要转换的语音的 base64 编码字符串, 要求 16000Hz 采样率的 wav 格式

    Returns:
        str: 转换后的文本
        None: 转换失败
    """
    params = gen_base_params()
    params['format'] = '2'  # wav
    params['speech'] = speech_base64
    params['rate'] = '16000'  # 16000Hz 采样率
    data = await do_post_request(STT_API_URL, params)
    return data['text'] if data else None


async def tts(text: str) -> Optional[str]:
    """
    文本转语音(语音合成).

    Args:
        text: 要转换的文本

    Returns:
        str: 转换后的语音的 base64 编码字符串, wav 格式
        None: 转换失败
    """
    params = gen_base_params()
    params['speaker'] = '6'  # 1: 普通话男声, 2: 静琪女声, 6: 欢馨女声, 7: 碧萱女声
    params['format'] = '2'  # wav
    params['volume'] = '0'
    params['speed'] = '100'
    params['aht'] = '0'
    params['apc'] = '58'
    params['text'] = text
    data = await do_post_request(TTS_API_URL, params)
    return data['speech'] if data else None


async def chat(question: str, session: str) -> Optional[str]:
    """
    智能闲聊.

    Args:
        question: 用户输入
        session: 会话标识（应用内唯一）

    Returns:
        str: 回复内容
        None: 获取回复失败
    """
    params = gen_base_params()
    params['question'] = question
    params['session'] = session
    data = await do_post_request(CHAT_API_URL, params)
    return data['answer'] if data else None
