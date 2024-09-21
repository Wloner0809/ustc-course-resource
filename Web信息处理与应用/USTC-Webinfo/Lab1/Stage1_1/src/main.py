from Movie import Movie
from Book import Book

if __name__ == "__main__":
    pre_url = 'https://movie.douban.com/subject/{}/'
    movie_path = '../Dataset/Movie_id.csv'
    movie_headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        'Cookie': 'll="118183"; bid=g_6HQFZOXUM; push_noty_num=0; push_doumail_num=0; __utmv=30149280.27464; _pk_id.100001.4cf6=8a2f4b34374d7db2.1695536824.; __yadk_uid=8r4Dy9vOaOBxlpcCWdkUjDWMkb4IvZgT; _vwo_uuid_v2=D1844E23FA7428890DF499EE695FD9BC1|00c7e01ae7f4b9a3ec12fa0b426758df; __utmz=223695111.1695819609.4.3.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; dbcl2="274649489:kmOdbLjv/84"; ap_v=0,6.0; __utmz=30149280.1696489439.11.3.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1696491180%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; __utma=223695111.308932955.1695536824.1696423252.1696491180.10; __utma=30149280.1856564355.1695534669.1696489439.1696496282.12; __utmt_douban=1; __utmb=30149280.2.10.1696496282'
    }
    movie_spider = Movie(pre_url, movie_path, movie_headers)
    movie_spider.run()

    # del movie_spider
    # pre_url = "https://book.douban.com/subject/{}/"
    # book_path = "../Dataset/Book_id.csv"
    # book_headers = {
    #     'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    #     'Cookie': 'll="118183"; bid=g_6HQFZOXUM; push_noty_num=0; push_doumail_num=0; __utmv=30149280.27464; dbcl2="274649489:kmOdbLjv/84"; ck=wpoA; frodotk_db="4834189140160095d89c49b3c04201bf"; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1696489439%2C%22https%3A%2F%2Fwww.google.com%2F%22%5D; _pk_id.100001.3ac3=c2e6df18537365a7.1696489439.; _pk_ses.100001.3ac3=1; ap_v=0,6.0; __utma=30149280.1856564355.1695534669.1696423249.1696489439.11; __utmc=30149280; __utmz=30149280.1696489439.11.3.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utma=81379588.665540426.1696489439.1696489439.1696489439.1; __utmc=81379588; __utmz=81379588.1696489439.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); _vwo_uuid_v2=D38FBE3F3F466B14320FFBF3574946190|8955e366bf5b36081b4754fdca91b8ca; __yadk_uid=RHrYNGnN7zwLHJQhscFwrmTOXsLPlvb2; __utmb=30149280.2.10.1696489439; __utmb=81379588.2.10.1696489439'
    # }
    # book_spider = Book(pre_url, book_path, book_headers)
    # book_spider.run()
