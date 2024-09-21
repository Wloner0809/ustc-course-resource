from Spider import Spider
from bs4 import BeautifulSoup
from typing import Dict, List, Any
import json
import re
import time
import random


class Book(Spider):
    # douban book spider
    def __init__(self, pre_url, book_id_path, header):
        super(Book, self).__init__(pre_url, book_id_path, header)
        self.book_id_list = self.get_id_list()
        self.error = []
        self.all_info = {}
        self.author = []
        self.count = 0

    def parse_text(self, text: str, book_id: str) -> Dict:
        soup = BeautifulSoup(text, "html.parser")
        # parse book title
        book_title = soup.find('span', property='v:itemreviewed')
        # book_title error solution
        if book_title is None:
            error_msg = book_id + "没有名称\n"
            print(error_msg)
            self.error.append(error_msg)
            book_title = ''
        else:
            book_title = book_title.text
        # parse book introduction
        book_intro = soup.find_all('div', attrs={'class': 'intro'})
        # book_intro error solution
        if book_intro is None:
            error_msg = book_id + "没有介绍\n"
            print(error_msg)
            self.error.append(error_msg)
            book_content_intro = ''
            book_author_intro = ''
        else:
            # solve no author or no (展开全部) condition
            if len(book_intro) >= 2:
                if book_intro[0].text.find("(展开全部)") == -1:
                    book_content_intro = book_intro[0].text.replace('\n', '')
                    if book_intro[1].text.find("(展开全部)") == -1:
                        book_author_intro = book_intro[1].text.replace('\n', '')
                    else:
                        book_author_intro = book_intro[2].text.replace('\n', '')
                else:
                    book_content_intro = book_intro[1].text.replace('\n', '')
                    if len(book_intro) == 2:
                        book_author_intro = ''
                    else:
                        if book_intro[2].text.find("(展开全部)") == -1:
                            book_author_intro = book_intro[2].text.replace('\n', '')
                        else:
                            book_author_intro = book_intro[3].text.replace('\n', '')
            elif len(book_intro) == 1:
                book_content_intro = book_intro[0].text.replace('\n', '')
                book_author_intro = ''
            else:
                book_content_intro = ''
                book_author_intro = ''
        # parse basic book info
        book_content = soup.find('div', attrs={'id': 'info'})
        single_book_dict = {"作者: ": "", "出版社: ": "", "出版年: ": "", "页数: ": "", "定价: ": "", "装帧: ": "",
                            "ISBN: ": ""}
        book_rating = ''
        number = []
        if book_content is None:
            error_msg = book_id + "没有基本信息"
            print(error_msg)
            self.error.append(error_msg)
            book_rating = ''
            number = [0, 0, 0]
        else:
            for info in single_book_dict.keys():
                match = re.search(info + r'(.*)$', book_content.text, re.M)
                if match:
                    single_book_dict[info] = match.group(1)
            book_rating = soup.find('div', attrs={'class': "rating_self clearfix"}).find(
                property='v:average')
            if book_rating is None:
                error_msg = book_id + "没有评分\n"
                print(error_msg)
                self.error.append(error_msg)
                book_rating = ''
            else:
                book_rating = book_rating.text.strip()
            # catch data of "want to read/ have read/ be reading"
            book_reading_data = soup.find('div', attrs={'id': 'collector'})
            if book_reading_data is None:
                error_msg = book_id + "没有想看\n"
                print(error_msg)
                self.error.append(error_msg)
                number = [0, 0, 0]
            else:
                book_reading_data = book_reading_data.find_all("p", class_="pl")
                number = []
                for data in book_reading_data:
                    link = data.find("a")
                    if link:
                        text = link.get_text()
                        numbers = re.search(r'\d+', text)
                        number.append(numbers.group())
        # single book info dictionary
        info = {"title": book_title, "author introduction": book_author_intro,
                "content introduction": book_content_intro, "rating": book_rating,
                "publish year": single_book_dict["出版年: "],
                "page num": single_book_dict["页数: "],
                "price": single_book_dict["定价: "],
                "wrapper": single_book_dict["装帧: "],
                "ISBN": single_book_dict["ISBN: "],
                "be_reading": str(number[0]), "have_read": str(number[1]), "wanna_read": str(number[2])}
        # add to one single dictionary
        self.all_info[book_id] = info
        return info

    def add_tag(self):
        tag_path = '../Dataset/Tag/Book_tag.csv'
        with open(tag_path, 'r', encoding='UTF-8') as f:
            lines = f.readlines()
            for line in lines:
                tag = line.strip('\n').split(',')
                self.all_info[tag[0]]['tag'] = tag[1].strip('"').split(',')

    def save_all_info_to_json(self):
        save_path = '../Result/Book_info.json'
        with open(save_path, 'w', encoding='UTF-8') as f:
            json.dump(self.all_info, f, indent=4, ensure_ascii=False)

    def save_error_message(self):
        save_path = '../Result/Book_error.csv'
        with open(save_path, 'w', encoding='UTF-8') as f:
            f.writelines(self.error)

    def parse_author(self, text: str):
        soup = BeautifulSoup(text, "html.parser")
        book_author = soup.find('div', attrs={'class': 'info'})
        if book_author is None:
            self.author.append("")
        else:
            book_author = book_author.text.split('\n')[1]
            self.author.append(book_author)

    def run(self):
        book_url = self.create_url()
        for index, book_id in enumerate(self.book_id_list):
            self.count += 1
            print(self.count, ". 正在爬取id为 {} 的书籍的信息".format(book_id))
            (text, status_code) = self.get_response(book_url[index], self.get_headers())
            (text, status_code) = self.get_response(book_url[index], self.cookie) if status_code == 404 else (
                text, status_code)
            # text, status_code = self.get_html(movie_url, headers)
            if status_code == 404:
                error_msg = '{}的资源不存在!\n'.format(book_id)
                print('    ' + error_msg)
                self.error.append(error_msg)
            else:
                self.parse_author(text)
                # self.all_info[book_id] = self.parse_text(text, book_id)
                print("    id为 {} 的书籍的信息爬取完毕\n".format(book_id))
            if self.count % 20 == 0:
                print("   ", time.ctime())
            time.sleep(random.uniform(0.5, 1))  # 休眠 0.5 ~ 1s
        load_path = '../Result/Book_info.json'
        with open(load_path, 'r', encoding='UTF-8') as f:
            full_info = json.load(f)
        for index, id_ in enumerate(self.id_list):
            full_info[id_]['author'] = self.author[index]
        save_path = '../Result/Book_info_new.json'
        with open(save_path, 'w', encoding='UTF-8') as f:
            json.dump(full_info, f, indent=4, ensure_ascii=False)
        # self.add_tag()
        # self.save_all_info_to_json()
        # self.save_error_message()
