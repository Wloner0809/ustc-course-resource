from typing import List, Any
import requests


class Spider:
    def __init__(self, pre_url, spider_path, header):
        self.pre_url = pre_url
        self.spider_path = spider_path
        self.id_list = []
        self.header = header
        self.url = []

    def get_id_list(self) -> List[str]:
        with open(self.spider_path, "r") as f:
            id = f.readlines()
            for id_single in id:
                self.id_list.append(id_single.rstrip())
        return self.id_list

    def create_url(self) -> List[str]:
        for id_ in self.id_list:
            self.url.append(self.pre_url + id_)
        return self.url

    def get_response(self, request_url: str):
        respond = requests.get(url=request_url, headers=self.header)
        return respond.text, respond.status_code
