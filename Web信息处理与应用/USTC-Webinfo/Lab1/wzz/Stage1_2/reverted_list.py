import json
import bisect
def invert(dict):
    inverted_list={}

    for key in dict:            
        for item in dict[key]:          #key:id item:str(name) 
            if item in inverted_list:
                index = bisect.bisect_left(inverted_list[item],key)
                if index != len(inverted_list[item]) and inverted_list[item][index] == key:       #保证不会将重复的id加入词项中
                    continue
                bisect.insort(inverted_list[item],key) #将key有序插入到列表中
            else:
                inverted_list[item] = [key]
    return inverted_list

if __name__ == "__main__":
    with open(r".\Lab1\wzz\Stage1_2\data\book_participle.json",'r', encoding='UTF-8') as fin:
        dict = json.load(fin)
    print (dict)
    #dict={1:"abc",3:"a",72:"abc",9:"bop",4:"adw",5:"adw",6:"a",7:"abc",8:"a",10:"bop",2:"bop"}
    inverted_list = invert(dict)
    with open(r".\Lab1\wzz\Stage1_2\data\reverted_dict_temp.json","w",encoding="UTF-8")as fout:
        json.dump(inverted_list, fout, indent=4, ensure_ascii=False)
    print (inverted_list)
