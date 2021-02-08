import time
import requests
import base64
import random
import os
from nonebot import get_driver

driver = get_driver()

def get_app_id() -> str:
    return driver.config.rt_app_id

def get_app_secret() -> str:
    return driver.config.rt_app_secret

async def get_joke():
    url = 'https://www.mxnzp.com/api/jokes/list/random'
    header = {'app_id': get_app_id(), 'app_secret': get_app_secret()}
    res = requests.get(url, headers=header)
    print(res.json())
    return res.json()['data'][0]['content']

async def get_history():
    url = 'https://www.mxnzp.com/api/history/today?type=1'
    header = {'app_id': get_app_id(), 'app_secret': get_app_secret()}
    res = requests.get(url, headers=header)
    ret = ''
    print(res.json())
    data = res.json()['data'][0]
    ret += '%s年%r月%r日' % (data['year'],data['month'],data['day']) + ': ' + f"{data['title']}" + '\n'
    ret += '[CQ:image,file=' + data['picUrl'] + ']'
    return ret

async def get_all(url,number = 0):
    if number == 20:
        return {'data': '翻译失败',
                'originLanguage': 'zh',
                'result': '翻译失败'}
    res = requests.get(url)
    try:
        return res.json()['data']
    except:
        return await get_all(url,number+1)


async def get_translation(source_text):
    url1 = 'https://www.mxnzp.com/api/convert/translate?content='
    source_lan = 'auto'
    target_lan = 'en'
    url2 = source_text + '&from=' + source_lan + '&to=' + target_lan
    url3 = f'&app_id={get_app_id()}&app_secret={get_app_secret()}'
    res = await get_all(url1 + url2 + url3)

    source_lan = res['originLanguage']
    if source_lan == 'zh':
        target_lan = 'en'
    else:
        target_lan = 'zh'
    url2 = source_text + '&from=' + source_lan + '&to=' + target_lan
    res = await get_all(url1 + url2 + url3)
    return res['result']


async def get_qrcode(source_text):
    url = 'https://www.mxnzp.com/api/qrcode/create/single?content=' + source_text + '&type=1'
    header = {'app_id': get_app_id(), 'app_secret': get_app_secret()}
    res = requests.get(url, headers=header)
    Base64_str = res.json()['data']['qrCodeBase64'][22:]
    figName = time.strftime("%Y-%m-%d%H-%M-%S", time.localtime()) + '-' + str(round(random.uniform(0, 100))) + '.jpg'
    fig_dir = os.path.join(os.getcwd(), 'nb2_bot', 'data','qrcode','images',figName)
    with open(fig_dir, mode='wb') as file_object:
        file_object.write(base64.b64decode(Base64_str))
    return '[CQ:image,file=file:///' + fig_dir + ']'

async def get_mobile_location(source_text):
    url = 'https://www.mxnzp.com/api/mobile_location/aim_mobile?mobile=' + source_text
    header = {'app_id': get_app_id(), 'app_secret': get_app_secret()}
    res = requests.get(url, headers=header)
    print(res.json())
    try:
        data = res.json().get('data')
        if data.get('province'):
            return '手机号 %s 的省份是 %s 运营商是 %s' % (data['mobile'], data['province'], data['carrier'])
        else:
            return '这似乎不是一个正确的手机号'
    except:
        return '这似乎不是一个正确的手机号'


