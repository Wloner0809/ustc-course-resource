import json
import bisect

class revert_dict:
    def revert(self):
        for key in self.dict:            
            for item in self.dict[key]:          #key:id item:str(name) 
                if item in self.reverted_dict:
                    if int(key) not in self.reverted_dict[item]:
                        index = bisect.bisect_left(self.reverted_dict[item],int(key))
                        bisect.insort(self.reverted_dict[item],int(key)) #将key有序插入到列表中
                else:
                    self.reverted_dict[item] = [int(key)]

    def __init__(self,dict):
        self.dict = dict
        self.reverted_dict = {}
        self.revert()

class Skip_revert_list(revert_dict):            #继承倒排表

    def __init__(self,dict):
        self.dict = dict
        revert_dict.__init__(self,dict)
        self.length = {}            #键：字符串     值：倒排表长度
        self.interval = {}          #键：字符串     值：跳表间隔
        self.skip_dict = {}         #键：字符串     值：List，由一系列跳表节点组成的列表
        self.list_head = {}         #键：字符串     值：skip_node对象
        self.create_skip_dict()
    
    def create_skip_list(self,word):
        self.length[word] = len(self.reverted_dict[word])
        self.interval[word] = int((self.length[word]) ** 0.5)
        self.list_head[word] = ((self.reverted_dict[word][0]), self.interval[word] if self.length[word]>1 else 0 , 0)
        self.skip_dict[word] = [self.list_head[word]]
        for i in range(self.interval[word], self.length[word] - self.interval[word], self.interval[word]):
            node = ((self.reverted_dict[word][i]), i + self.interval[word], i)       #(value,next,down)
            self.skip_dict[word].append(node)
        last = len(self.skip_dict[word])*self.interval[word]
        if last < len(self.reverted_dict[word])-1:
            node = ((self.reverted_dict[word][last]),len(self.reverted_dict[word])-1,last)
            self.skip_dict[word].append(node)
    def create_skip_dict(self):
        for key in self.reverted_dict.keys():
            self.create_skip_list(key)

if __name__ == "__main__":
    with open(r"D:\web_lab\WebInfo\Lab1\wy\Stage1_2\Result\Book_keyword.json","r",encoding="UTF-8") as fin:
        participle_dict = json.load(fin)
    skip = Skip_revert_list(participle_dict)
    skip.create_skip_dict()
    with open(r"D:\web_lab\WebInfo\Lab1\wzz\Stage1_2\data\Book_reverted_dict.json","w",encoding="UTF-8") as fout_reverted_dict:
        json.dump(skip.reverted_dict,fout_reverted_dict, indent=4, ensure_ascii=False)
    with open(r"D:\web_lab\WebInfo\Lab1\wzz\Stage1_2\data\Book_skip_dict.json","w",encoding="UTF-8") as fout_skip_dict:
        json.dump(skip.skip_dict,fout_skip_dict, indent=4, ensure_ascii=False)