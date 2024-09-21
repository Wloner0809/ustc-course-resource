import re
from ua_pool import UAPool
import random
import time
from bs4 import BeautifulSoup
import requests
import json

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    'Cookie': 'll="118183"; bid=g_6HQFZOXUM; push_noty_num=0; push_doumail_num=0; __utmv=30149280.27464; _pk_id.100001.4cf6=8a2f4b34374d7db2.1695536824.; __yadk_uid=8r4Dy9vOaOBxlpcCWdkUjDWMkb4IvZgT; _vwo_uuid_v2=D1844E23FA7428890DF499EE695FD9BC1|00c7e01ae7f4b9a3ec12fa0b426758df; __utmz=30149280.1695819609.5.2.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmz=223695111.1695819609.4.3.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmc=30149280; __utmc=223695111; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1696423247%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_ses.100001.4cf6=1; ap_v=0,6.0; __utma=30149280.1856564355.1695534669.1696419830.1696423249.10; __utma=223695111.308932955.1695536824.1696419855.1696423252.9; __utmb=223695111.0.10.1696423252; frodotk_db="cea7e8878f16a5f76bf7b996ad43f1e5"; dbcl2="274649489:kmOdbLjv/84"; ck=wpoA; __utmb=30149280.16.10.1696423249'
}


class Spider:
    def __init__(self):
        self.prefix_url = 'https://movie.douban.com/subject/{}/'
        self.headers = {}
        self.user_agent_pool = UAPool()
        self.id_list = []

    def get_headers(self) -> dict:
        self.headers['User-Agent'] = self.user_agent_pool.pop_pool()
        return self.headers

    def get_id_list(self, spider_file_path) -> list:
        with open(spider_file_path, "r") as f:
            id_list_n = f.readlines()  # 有换行符
            [self.id_list.append(line.strip()) for line in id_list_n]  # 无换行符
            return self.id_list

    def get_url(self, spider_id):
        return self.prefix_url.format(spider_id)

    def get_html(self, url, headers):
        response = requests.get(url=url, headers=headers)
        text = response.text.encode('UTF-8')
        status_code = response.status_code
        return text, status_code


class Movie(Spider):

    def __init__(self, movie_id_path):
        super(Movie, self).__init__()
        self.movie_id_list = self.get_id_list(movie_id_path)
        self.movie_id_path = movie_id_path
        self.error = []
        self.all_info = {}
        self.count = 0

    def parse_text(self, text, movie_id):
        # 这里应当维护一个字典 info ，包含了需要爬取的有效信息，结构应当为
        # {'name': ' ', 'type': ' ', 'director': ' ', 'characters': ['', '', '', ...], ...}
        info = {}
        soup = BeautifulSoup(text, 'html.parser')
        """
            提取影片名
        """
        name = soup.find('span', {'property': 'v:itemreviewed'})
        if name is None:
            error_msg = movie_id + "没有名称\n"
            print(error_msg)
            self.error.append(error_msg)
            info['name'] = ''
        else:
            info['name'] = name.text
        """
            提取想看的人数
        """
        favor = soup.find('a', {'href': "https://movie.douban.com/subject/{}/comments?status=P".format(movie_id)})
        if favor is None:
            error_msg = movie_id + "没有想看人数的信息\n"
            print(error_msg)
            self.error.append(error_msg)
            info['favor'] = ''
        else:
            match = re.search(r'(\d+)', favor.text)
            info['favor'] = match.group(1) if match else ''
        """
            提取看过的人数
        """
        watched = soup.find('a', {'href': "https://movie.douban.com/subject/{}/comments?status=F".format(movie_id)})
        if watched is None:
            error_msg = movie_id + "没有看过人数的信息\n"
            print(error_msg)
            self.error.append(error_msg)
            info['watched'] = ''
        else:
            match = re.search(r'(\d+)', watched.text)
            info['watched'] = match.group(1) if match else ''
        """
            提取包括导演，主演等信息
        """
        main_info = soup.find('div', {'id': 'info'})
        match_list = {'导演: ': '', '编剧: ': '', '主演: ': '', '类型: ': '', '制片国家/地区: ': '', '语言: ': '',
                      '上映日期: ': '', '片长: ': '', '又名: ': '', 'IMDb: ': ''}
        if main_info is None:
            error_msg = movie_id + "没有导演等主要信息\n"
            print(error_msg)
            self.error.append(error_msg)
        else:
            for item in match_list.keys():
                match = re.search(item + r'(.*)$', main_info.text, re.M)  # re.M 表示用行匹配
                if match:
                    match_list[item] = match.group(1)
                else:
                    error_msg = movie_id + "中'" + item + "'没有对应匹配\n"
                    print(error_msg)
                    self.error.append(error_msg)
                    match_list[item] = ''
        info['director'] = match_list['导演: '].split(' / ')
        info['characters'] = match_list['主演: '].split(' / ')
        info['playwright'] = match_list['编剧: '].split(' / ')
        info['type'] = match_list['类型: '].split(' / ')
        info['country_or_region'] = match_list['制片国家/地区: '].split(' / ')
        info['language'] = match_list['语言: '].split(' / ')
        info['release_date'] = match_list['上映日期: '].split(' / ')  # 可能不同地区有多个上映日期
        info['film_length'] = match_list['片长: '].split(' / ')  # 可能有加长版
        info['alias'] = match_list['又名: '].split(' / ')
        info['IMDb'] = match_list['IMDb: ']
        """
            提取简要介绍
        """
        intro = soup.find('span', {'class': 'all hidden'})
        intro = soup.find('span', {'property': 'v:summary'}) if intro is None else intro
        if intro is None:
            error_msg = movie_id + "没有介绍\n"
            print(error_msg)
            self.error.append(error_msg)
            info['intro'] = ''
        else:
            intro_text = intro.text.replace('\n', '').replace('\r', '')  # Windows下两个要同时去除
            intro_text = intro_text.replace('　', '').strip()  # 注意这里是 全角空格
            intro_text = intro_text.replace('  ', '')  # 尽量去除中间的空格, 最终只会留下最多一个空格
            info['intro'] = intro_text

        return info

    def save_all_info_to_json(self):
        index = self.movie_id_path.rfind('/')
        save_path = self.movie_id_path[0:index] + '/Movie_info.json' if index != -1 else 'Movie_info.json'
        with open(save_path, 'w', encoding='UTF-8') as f:
            json.dump(self.all_info, f, indent=4, ensure_ascii=False)

    def save_error_message(self):
        index = self.movie_id_path.rfind('/')
        save_path = self.movie_id_path[0:index] + '/Movie_error.txt' if index != -1 else 'Movie_error.txt'
        with open(save_path, 'w', encoding='UTF-8') as f:
            f.writelines(self.error)

    def run(self):
        for movie_id in self.movie_id_list:
            self.count += 1
            print(self.count, ". 正在爬取id为 {} 的电影的信息".format(movie_id))
            movie_url = self.get_url(movie_id)
            (text, status_code) = self.get_html(movie_url, self.get_headers())
            (text, status_code) = self.get_html(movie_url, headers) if status_code == 404 else (text, status_code)
            # text, status_code = self.get_html(movie_url, headers)
            if status_code == 404:
                error_msg = '{}的资源不存在!\n'.format(movie_id)
                print('    ' + error_msg)
                self.error.append(error_msg)
            else:
                self.all_info[movie_id] = self.parse_text(text, movie_id)
                print("    id为 {} 的电影的信息爬取完毕\n".format(movie_id))
            if self.count % 20 == 0:
                print("   ", time.ctime())
            time.sleep(random.uniform(1.5, 2))  # 休眠 0.5 ~ 1s
        self.save_all_info_to_json()
        self.save_error_message()


if __name__ == '__main__':
    movie_path = '../Dataset/Movie_id_tmp1.csv'
    movie_spider = Movie(movie_path)
    movie_spider.run()
