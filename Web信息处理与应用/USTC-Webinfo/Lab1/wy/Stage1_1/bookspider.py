from Spider import Spider
import bs4
from typing import Dict, List, Any
import json
import re


class bookSpider(Spider):
    # douban book spider
    def __init__(self, pre_url, spider_path, header):
        super(bookSpider, self).__init__(pre_url, spider_path, header)
        self.book_dict = {}

    def parse_html(self, text: str, id_single: str) -> Dict:
        soup = bs4.BeautifulSoup(text, "html.parser")
        # parse book title
        book_title = soup.find('span', property='v:itemreviewed').text
        # parse book introduction
        book_intro = soup.find_all('div', attrs={'class': 'intro'})
        # solve no author or no (展开全部) condition
        if len(book_intro) >= 2:
            if book_intro[0].text.find("(展开全部)") == -1:
                book_content_intro = book_intro[0].text.replace('\n', '')
                book_author_intro = book_intro[2].text.replace('\n', '')
            else:
                if len(book_intro[1].text.rstrip()) > len(book_intro[0].text.rstrip()):
                    book_content_intro = book_intro[1].text.replace('\n', '')
                else:
                    book_content_intro = book_intro[0].text.replace('\n', '')
                book_author_intro = book_intro[2].text.replace('\n', '')
        else:
            if len(book_intro[1].text.rstrip()) > len(book_intro[0].text.rstrip()):
                book_content_intro = book_intro[1].text.replace('\n', '')
            else:
                book_content_intro = book_intro[0].text.replace('\n', '')
            book_author_intro = None
        # parse basic book info
        book_content = soup.find('div', attrs={'id': 'info'})
        single_book_dict = {"作者": "", "出版社": "", "出版年": "", "页数": "", "定价": "", "装帧": "", "ISBN": ""}
        for info in single_book_dict.keys():
            match = re.search(info + r'(.*)$', book_content.text, re.M)
            if match:
                single_book_dict[info] = match.group(1)
        book_rating = soup.find('div', attrs={'class': "rating_self clearfix"}).find(property='v:average').text.strip()
        # catch data of "want to read/ have read/ be reading"
        book_reading_data = soup.find('div', attrs={'id': 'collector'})
        book_reading_data = book_reading_data.find_all("p", class_="pl")
        number = []
        for data in book_reading_data:
            link = data.find("a")
            if link:
                text = link.get_text()
                numbers = re.search(r'\d+', text)
                number.append(numbers.group())
        # single book info dictionary
        Book_info_dict = {"title": book_title, "author introduction": book_author_intro,
                          "content introduction": book_content_intro, "rating": book_rating,
                          "publish year": single_book_dict["出版年"].split(': ')[1],
                          "page num": single_book_dict["页数"].split(': ')[1],
                          "price": single_book_dict["定价"].split(': ')[1],
                          "wrapper": single_book_dict["装帧"].split(': ')[1],
                          "ISBN": single_book_dict["ISBN"].split(': ')[1],
                          "be_reading": str(number[0]), "have_read": str(number[1]), "wanna_read": str(number[2])}
        # add to one single dictionary
        self.book_dict[id_single] = Book_info_dict
        return Book_info_dict

    def save_to_json(self):
        with open("test.json", "w", encoding='utf-8') as f:
            json.dump(self.book_dict, f, indent=4, ensure_ascii=False)
