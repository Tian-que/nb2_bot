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

    def article_new(self, tittle: str, text):
        
        data = {
            "title": tittle,
            "text": ujson.dumps(text),
            "desc": "命运2日报",
            "post_type": "2",
            "draft": "0",
            "words_count": "300",
            "hashtags": "[\"命运2日报\"]",
            "topic_ids": "65410",
            "link_tag": "11",
            "thumb": "https://imgheybox.max-c.com/web/2022/01/13/37625d1c145c6cfc99866bbf725f02e1.jpeg",
            "original": "1",
            "declaration": "2",
        }
        c = self.call_api(url='https://api.xiaoheihe.cn/bbs/app/api/link/post', data = data)
        return c['link_id']

    def article_edit(self,tittle: str,text,link_id: str or int):
        data = {
            "title": tittle,
            "text": ujson.dumps(text),
            "desc": "命运2日报",
            "post_type": "2",
            "draft": "0",
            "words_count": "300",
            "hashtags": "[\"命运2日报\"]",
            "topic_ids": "65410",
            "link_tag": "11",
            "thumb": "https://imgheybox.max-c.com/web/2022/01/13/37625d1c145c6cfc99866bbf725f02e1.jpeg",
            "original": "1",
            "declaration": "2",
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
        img_dir = self.check_upload_img_size(img_dir)
        name, src = self.post_wiki_img(img_dir)
        article_info = self.create_wiki_article(name, src)
        self.update_wiki_today_report(article_info)
        return src

    def post_img_old(self,img_dir: str):
        t = int(time.time())
        url = f'https://api.xiaoheihe.cn/bbs/qiniu/upload/images/?os_type=web&version=999.0.0&hkey={self.get_hkey(t)}&_time={t}&water_mark=0&heybox_id={self.heybox_id}'
        img_dir = self.check_upload_img_size(img_dir)
        img_name = img_dir.split('\\')[-1]
        img_type = img_dir.split('.')[-1]
        files = {'picture': (img_name, open(img_dir, 'rb'), f'image/{img_type}')}
        response = requests.post(url=url, headers=self.headers, files=files, cookies=self.cookie)
        c = response.json()
        if c['status'] != 'ok':
            raise
        else:
            return c['result']['img_list'][0]

    def check_upload_img_size(self, imgDir: str) -> str:
        im = Image.open(imgDir)
        im = im.convert('RGB')
        quality = 100
        imgDir = imgDir[:-3] + 'jpg'
        im.save(imgDir, quality=quality)
        return imgDir

    def post_wiki_img(self, img_dir: str):
        # 获取 token
        img_name = img_dir.split('\\')[-1]
        img_type = img_dir.split('.')[-1]
        data = {
            "wiki_id": "1085660",
            "name": img_name
        }
        c = self.call_api(url="https://api.xiaoheihe.cn/wiki/get_upload_img_qiniu_token/", data = data)

        # 上传图片
        ret = self.upload_qiniup_com(key = c['result']['key'],token = c['result']['token'],img_dir = img_dir)
        return img_name.split('.')[0], "https://cdn.max-c.com/" + ret

    def upload_qiniup_com(self, key: str, token: str, img_dir: str):

        url = "https://upload.qiniup.com/"
        data = {
            "key": key,
            "token": token,
        }
        img_name = img_dir.split('\\')[-1]
        img_type = img_dir.split('.')[-1]
        files = {'file': (img_name, open(img_dir, 'rb'), f'image/{img_type}')}

        headers = {
            'Referer':'https://c.xiaoheihe.cn/',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0'
            }

        response = requests.post(url=url, headers=headers, data = data, files = files)
        c = response.json()
        if c['status'] != 'ok':
            raise
        else:
            return c['key']

    def get_article_info(self, name):
        t = int(time.time())
        url = f'https://api.xiaoheihe.cn/wiki/get_article_list/?wiki_id=1085660&query={name}&offset=0&limit=100os_type=web&version=999.0.0&hkey={self.get_hkey(t)}&_time={t}&heybox_id={self.heybox_id}'
        response = requests.post(url=url,headers=self.headers, cookies = self.cookie)
        c = response.json()
        if c['status'] != 'ok':
            raise
        if c['result']['count'] == 0:
            return 0
        return c['result']['articles'][0]

    def create_wiki_article(self, name, img_src):
        article_info = self.get_article_info(name)
        if not article_info:
            data = {
                "article_type": "1",
                "game_id": "1085660",
                "name": name,
                "text": f"<p><img src=\"{img_src}\" style=\"max-width:100%;\">"
            }
            self.call_api(url="https://api.xiaoheihe.cn/wiki/create_article/", data = data)
            article_info = self.get_article_info(name)
        return article_info

    def update_wiki_today_report(self, article_info):
        t = int(time.time())
        url = f'https://api.xiaoheihe.cn/wiki/change_home_block_entry_info/'
        payload = {
            "wiki_id": 1085660,
            "entry_id": 9767026,
            "tag_id": 9767023,
            "entry_type": 1,
            "entry_name": "命运2日报",
            "entry_img": "https://cdn.max-c.com/wiki/1085660/日报头图.jpg?v=1",
            "entry_url": f"https://api.xiaoheihe.cn/wiki/get_article_for_app/?article_id={article_info['article_id']}&wiki_id=1085660",
            "entry_desc": "@每日1:03自动更新(测试中)",
            "cover_type": 1,
            "article_id": article_info['article_id'],
            "article_name": article_info['article_name'],
            "os_type": "web",
            "version": "999.0.0",
            "hkey": self.get_hkey(t),
            "_time": t,
            "heybox_id": self.heybox_id
        }
        response = requests.post(url=url,headers=self.headers, cookies = self.cookie, params=payload)
        c = response.json()

    def update_wiki(self, img_dir: str):
        name, src = self.post_wiki_img(img_dir)
        article_info = self.create_wiki_article(name, src)
        self.update_wiki_today_report(article_info)
        return src
h_tq = heyboxapi(user_pkey='MTY0MjQwNjAxNy44NV8yMzc0MzEyOXlldWNhem9pd2loZ2Zra2I__',heybox_id=23743129)
h = heyboxapi(user_pkey='MTYzMjU0NTQwMS42MV8xODcwNzI2NmJlYW5zd2t2cXplcmZtY3g__',heybox_id=18707266)
if __name__ == "__main__":
    name, src = h.post_wiki_img(img_dir = 'D:\\Desktop\\命运2日报2022-01-17.png')
    # article_info = h.create_wiki_article(name, src)
    # h.update_wiki_today_report(article_info)
    a = 1