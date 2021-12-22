import aiohttp
import os
import requests
import difflib


# 读取配置文件函数
async def read_file(file_name):
    file_handle = open(file_name, 'r')
    text = file_handle.read().splitlines()  # 读取后以行进行分割
    file_handle.close()
    return text[1:text.index('')]


# 比较两个文件并输出结果
async def compare_file(file1_name, file2_name) -> list:
    text1_lines = await read_file(file1_name)
    text2_lines = await read_file(file2_name)
    diff = difflib.Differ()  # 创建htmldiff 对象
    result = diff.compare(text1_lines, text2_lines)  # 通过make_file 方法输出 html 格式的对比结果
    #  将结果保存到result.html文件中并打开
    result = {i.split()[1].strip('"'): int(i.split()[3]) for i in result if i[0] == '+'}
    return [[i for i,j in result.items()], sum([j for i,j in result.items()])]

async def StrOfSize(size):
    async def strofsize(integer, remainder, level):
        if integer >= 1024:
            remainder = integer % 1024
            integer //= 1024
            level += 1
            return await strofsize(integer, remainder, level)
        else:
            return integer, remainder, level

    units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    integer, remainder, level = await strofsize(size, 0, 0)
    if level+1 > len(units):
        level = -1
    return ( '{}.{:>03d} {}'.format(integer, remainder, units[level]) )


async def download_file(url: str, filename: str):
    figdir = os.path.dirname(filename)
    if not os.path.exists(figdir):
        os.makedirs(figdir)

    async with aiohttp.ClientSession() as session:
        response = await session.get(url, verify_ssl=False)
        content = await response.read()

    with open(filename, 'wb') as f:
        f.write(content)
    return 1

async def write_file(data: str, filename: str):
    figdir = os.path.dirname(filename)
    if not os.path.exists(figdir):
        os.makedirs(figdir)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(data)
    return 1

async def paste(code):
    url1 = 'https://netcut.cn/api/note/update/'
    url2 = 'https://netcut.cn/4er7ucs8kfg0'
    data = {
        "note_id": (None, "624e25a60d56cd0a"),
        "note_content": (None, code)
    }
    r = requests.post(url1, files = data,verify=False)
    status = r.json().get('status')
    return url2 if status == 1 else None
