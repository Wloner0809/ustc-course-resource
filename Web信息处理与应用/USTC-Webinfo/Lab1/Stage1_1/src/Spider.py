from typing import List, Any
import requests
from ua_pool import UAPool


class Spider:
    def __init__(self, pre_url, spider_path, cookie):
        self.pre_url = pre_url
        self.spider_path = spider_path
        self.id_list = []
        self.cookie = cookie  # 用cookie时调用这个cookie属性
        self.headers = {}
        self.user_agent_pool = UAPool()
        self.url = []

    def get_headers(self) -> dict:
        self.headers['User-Agent'] = self.user_agent_pool.pop_pool()
        return self.headers

    def get_id_list(self) -> List[str]:
        with open(self.spider_path, "r") as f:
            id = f.readlines()
            for id_single in id:
                self.id_list.append(id_single.rstrip())
        return self.id_list

    def create_url(self) -> List[str]:
        for id_ in self.id_list:
            self.url.append(self.pre_url.format(id_))
        return self.url

    def get_response(self, request_url: str, headers: dict):
        respond = requests.get(url=request_url, headers=headers)
        return respond.text, respond.status_code
