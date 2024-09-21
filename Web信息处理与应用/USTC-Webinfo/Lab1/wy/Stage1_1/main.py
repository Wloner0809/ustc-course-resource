import time
from bookspider import bookSpider

if __name__ == "__main__":
    pre_url = "https://book.douban.com/subject/"
    spider_path = "tmp.csv"
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        "Cookie": 'talionnav_show_app="0"; bid=IACqUpGr3BI; ll="118183"; _gid=GA1.2.188759274.1695820852; Hm_lvt_6d4a8cfea88fa457c3127e14fb5fabc2=1695820707,1695826676; _ck_desktop_mode=1; vmode=pc; ap_v=0,6.0; __utma=30149280.1597997478.1695697539.1695820858.1695826682.4; __utmb=30149280.0.10.1695826682; __utmc=30149280; __utmz=30149280.1695826682.4.3.utmcsr=m.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; push_noty_num=0; push_doumail_num=0; frodotk_db="d80ef85ad4c6cb19882ce9107e54614b"; frodotk="2ab41f9fd6abb122801c5edf84031366"; talionusr="eyJpZCI6ICIyNzQ2NDkzOTgiLCAibmFtZSI6ICJwYXN0ZWwifQ=="; dbcl2="274649398:3hMXRXBKzYg"; ck=JPGb; Hm_lpvt_6d4a8cfea88fa457c3127e14fb5fabc2=1695827445; _ga_Y4GN1R87RG=GS1.1.1695826676.2.1.1695827446.0.0.0; _ga=GA1.2.1856646815.1695820852"'
    }
    book_spider_sample = bookSpider(pre_url, spider_path, header)
    book_spider_sample.get_id_list()
    book_spider_sample.create_url()
    for index, id_ in enumerate(book_spider_sample.id_list):
        print("catch book {} now!".format(id_))
        text, status_code = book_spider_sample.get_response(book_spider_sample.url[index])
        if status_code != 200:
            print("error")
            raise"request error"
        else:
            book_spider_sample.parse_html(text, id_)
        time.sleep(1)
    book_spider_sample.save_to_json()
