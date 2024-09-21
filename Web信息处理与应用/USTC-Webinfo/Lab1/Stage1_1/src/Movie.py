import re
import random
import time
from bs4 import BeautifulSoup
import json
from Spider import Spider


class Movie(Spider):

    def __init__(self, pre_url, movie_id_path, header):
        super(Movie, self).__init__(pre_url, movie_id_path, header)
        self.movie_id_list = self.get_id_list()
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

    def add_tag(self):
        tag_path = '../Dataset/Tag/Movie_tag_temp.csv'
        with open(tag_path, 'r', encoding='UTF-8') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip('\n')
                index = line.find(',')
                if index != -1:
                    movie_id = line[0:index]
                    tag = line[index + 1:]
                    # print(movie_id, ' ', tag)
                self.all_info[movie_id]['tag'] = tag.strip('"').split(',')

    def save_all_info_to_json(self):
        save_path = '../Result/Movie_info.json'
        with open(save_path, 'w', encoding='UTF-8') as f:
            json.dump(self.all_info, f, indent=4, ensure_ascii=False)

    def save_error_message(self):
        save_path = '../Result/Movie_error.csv'
        with open(save_path, 'w', encoding='UTF-8') as f:
            f.writelines(self.error)

    def run(self):
        movie_url = self.create_url()
        for index, movie_id in enumerate(self.movie_id_list):
            self.count += 1
            print(self.count, ". 正在爬取id为 {} 的电影的信息".format(movie_id))
            (text, status_code) = self.get_response(movie_url[index], self.get_headers())
            (text, status_code) = self.get_response(movie_url[index], self.cookie) if status_code == 404 else (
                text, status_code)
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
            time.sleep(random.uniform(0.5, 1))  # 休眠 0.5 ~ 1s
        self.add_tag()
        self.save_all_info_to_json()
        self.save_error_message()
