import requests
import hashlib
import time
import ujson


class heyboxapi:
    def __init__(self,user_pkey,heybox_id):
        self.cookie = {i.split("=")[0]: i.split("=")[-1] for i in f'user_pkey={user_pkey}'.split("; ")}
        self.heybox_id = heybox_id
        self.headers = {
            'Referer':'https://www.xiaoheihe.cn/',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0',
            }

    def call_api(self, url: str, **kwargs):
        t = int(time.time())
        url += f'?os_type=web&version=999.0.0&hkey={self.get_hkey(t)}&_time={t}&heybox_id={self.heybox_id}'
        response = requests.post(url=url,headers=self.headers, cookies = self.cookie, **kwargs)
        c = response.json()
        if c['status'] != 'ok':
            raise
        else:
            return c

    def get_hkey(self, t: int) -> str:
        def get_md5(data: str):
            md5 = hashlib.md5()
            md5.update(data.encode('utf-8'))
            result = md5.hexdigest()
            return (result)

        h = "web/_time=" + str(t)
        h = get_md5(h)
        h = h.replace('b', 'web')
        h = get_md5(h)
        return (h)

    def article_new(self,tittle: str,text :[]):
        data = {
            "title": tittle,
            "text": ujson.dumps(text),
            "link_tag": "11",
            "topic_ids": "65410",
            "desc": "啦啦啦啦啦啦",
            "post_type": "1",
            "draft": "1",
            "words_count": "50",
            "hashtags": "[\"命运2日报\"]",
        }
        c = self.call_api(url='https://api.xiaoheihe.cn/bbs/app/api/link/post', data = data)
        return c['link_id']

    def article_edit(self,tittle: str,text: [],link_id: str or int):
        data = {
            "title": tittle,
            "text": ujson.dumps(text),
            "link_tag": "11",
            "topic_ids": "65410",
            "desc": "啦啦啦",
            "post_type": "1",
            "draft": "1",
            "words_count": "40",
            "hashtags": "[]",
            "link_id": f"{link_id}",
            "edit": "1",
        }
        c = self.call_api(url='https://api.xiaoheihe.cn/bbs/app/api/link/post',data = data)
        return c

    def article_delete(self,link_id: str or int):
        data = {
            "link_id": f"{link_id}"
        }
        c = self.call_api(url="https://api.xiaoheihe.cn/bbs/app/link/delete", data = data)
        return c

    def post_img(self,img_dir: str):
        img_name = img_dir.split('\\')[-1]
        img_type = img_dir.split('.')[-1]
        files = {'picture': (img_name, open(img_dir, 'rb'), f'image/{img_type}')}
        c = self.call_api(url='https://api.xiaoheihe.cn/bbs/qiniu/upload/images/',files=files)
        return c['result']['img_list'][0]


h = heyboxapi(user_pkey='MTYxNTg5OTA5Mi41N18yMzc0MzEyOWxkc3pjZmV1cWZlc25xbXI__',heybox_id=23743129)