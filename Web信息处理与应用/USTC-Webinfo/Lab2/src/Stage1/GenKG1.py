import Extract
import Filter

# 获取基础数据
base_entities = set()
with open('../data/douban2fb.txt', 'r') as f:
    for i in f.readlines():
        _id, entity = i.strip().split()
        base_entities.add("<http://rdf.freebase.com/ns/{}>".format(entity))
print("获取基础数据完成。")

freebase_path = '../data/freebase_douban.gz'

Entity_path_1 = '../data/douban2fb.txt'
KG_path_1 = '../result/KG_path_1.txt.gz'
entities_set_1 = Extract.ExtractId2Entity(Entity_path_1)
Extract.ExtractFreebase2Step(freebase_path, KG_path_1, entities_set_1)
print("第一跳子图构建完成。")

filter_1 = Filter.Filter(KG_path_1, 40, 20000, 50, 'second')

entities_set_filter_1, relation_set_filter_1 = Extract.ExtractList2Entity(
    filter_1.triple_list)
for i in base_entities:
    assert (i in entities_set_filter_1)
print("第一跳子图验证完成。")
print("第一跳共有三元组：", len(filter_1.triple_list))
print("第一跳共有实体：", len(entities_set_filter_1))
print("第一跳共有关系：", len(relation_set_filter_1))

triple_list_1 = filter_1.filter()
KG_filter_path_1 = '../result/KG_filter_path_1.txt'
filter_1.save(KG_filter_path_1)
print("第一跳子图过滤完成。")

entities_set_filter_1, relation_set_filter_1 = Extract.ExtractList2Entity(
    triple_list_1)
print("第一跳过滤后共有三元组：", len(triple_list_1))
print("第一跳过滤后共有实体：", len(entities_set_filter_1))
print("第一跳过滤后共有关系：", len(relation_set_filter_1))
