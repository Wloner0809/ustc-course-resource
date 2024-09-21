import json
import requests

# path = '../Dataset/Book_id.csv'
# save_path = path[:path.rfind('/')] + '/Movie_info.json'
# print(save_path)
#
# dict1 = {'name': 'Melmaphother', 'type': 'Person', 'director': 'a', 'characters': {'1': 'b', '2': 'v', '3': 'c'}}
# dict2 = {'name': 'Melmaphother', 'type': 'Person', 'director': 'a', 'characters': ['b', 'v', 'c']}
# # json文件中支持数组 [], 所以主演可以用 dict2 形式表示
# dict3 = {'1234567': dict2}
#
# with open(save_path, 'w') as f:
#     json.dump(dict1, f, indent=4)
#
#     json.dump(dict2, f, indent=4)
#     json.dump(dict3, f, indent=4)

# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
#                  AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
# }
#
#
# def get_html(url):
#     response = requests.get(url=url, headers=headers)
#     text = response.text
#     status_code = response.status_code
#     return text, status_code
#
#
# text, status_code = get_html('https://movie.douban.com/subject/1292052/')
# with open('douban.html', 'w', encoding='UTF-8') as f:
#     f.write(text)
# print(status_code)


# from bs4 import BeautifulSoup
#
# def string_to_ascii(input_string):
#     ascii_result = []
#     for char in input_string:
#         ascii_value = ord(char)
#         ascii_result.append(ascii_value)
#
#     return ascii_result
#
#
# with open('douban.html', 'r', encoding='UTF-8') as f:
#     text = f.read()
#
# # print(text)
# info = {}
#
#
# def parse_text(movie_id, text):
#     # 这里应当维护一个字典 info ，包含了需要爬取的有效信息，结构应当为
#     # {'name': ' ', 'type': ' ', 'director': ' ', 'characters': ['', '', '', ...], ...}
#     soup = BeautifulSoup(text, 'html.parser')
#     name = soup.find('span', {'property': 'v:itemreviewed'})
#     if name is None:
#         print(movie_id, "没有名称\n")
#         return None
#     # print(name.text)
#     info['name'] = name.text
#     main_info = soup.find('div', {'id': 'info'})
#     # print(main_info.text)
#     if main_info is None:
#         print(movie_id, "没有导演等主要信息\n")
#         return None
#     info['main_info'] = main_info.text
#
#     intro = soup.find('span', {'class': "all hidden"})
#     if intro is None:
#         print(movie_id, "没有介绍\n")
#         return None
#     intro_text = intro.text.replace('\n', '').replace('\r', '')
#     intro_text = intro_text.replace('　', '').replace(' ', '')
#     print(string_to_ascii(intro_text))
#     print(intro_text)
#     info[intro] = intro_text
#
#
# parse_text('1111111', text)

# main_info.text 的结果
# 剥离出对应的信息

# 导演: 弗兰克·德拉邦特
# 编剧: 弗兰克·德拉邦特 / 斯蒂芬·金
# 主演: 蒂姆·罗宾斯 / 摩根·弗里曼 / 鲍勃·冈顿 / 威廉姆·赛德勒 / 克兰西·布朗 / 吉尔·贝罗斯 / 马克·罗斯顿 / 詹姆斯·惠特摩 / 杰弗里·德曼 / 拉里·布兰登伯格 / 尼尔·吉恩托利 / 布赖恩·利比 / 大卫·普罗瓦尔 / 约瑟夫·劳格诺 / 祖德·塞克利拉 / 保罗·麦克兰尼 / 芮妮·布莱恩 / 阿方索·弗里曼 / V·J·福斯特 / 弗兰克·梅德拉诺 / 马克·迈尔斯 / 尼尔·萨默斯 / 耐德·巴拉米 / 布赖恩·戴拉特 / 唐·麦克马纳斯
# 类型: 剧情 / 犯罪
# 制片国家/地区: 美国
# 语言: 英语
# 上映日期: 1994-09-10(多伦多电影节) / 1994-10-14(美国)
# 片长: 142分钟
# 又名: 月黑高飞(港) / 刺激1995(台) / 地狱诺言 / 铁窗岁月 / 消香克的救赎
# IMDb: tt0111161
