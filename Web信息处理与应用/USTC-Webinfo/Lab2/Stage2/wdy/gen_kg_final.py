kg_path = 'stage2\wdy\KG_filter_path_2.txt'
douban2fb_path = 'stage2\wdy\douban2fb.txt'
movie_id_map_path = 'stage2\movie_id_map.txt'
kg_final_path = 'stage2\stage2\data\Douban\kg_final.txt'

douban2fb = {}
with open(douban2fb_path, 'r') as f:
    for line in f:
        line = line.strip().split()
        douban2fb[line[0]] = line[1]

movie_id_map = {}
with open(movie_id_map_path, 'r') as f:
    for line in f:
        line = line.strip().split()
        movie_id_map[line[0]] = line[1]

entity2id = {}
for douban_id, fb_id in douban2fb.items():
    _id = movie_id_map[douban_id]
    entity = "<http://rdf.freebase.com/ns/{}>".format(fb_id)
    entity2id[entity] = _id

entities = set()
relations = set()
triplet_num = 0
with open(kg_path, 'r') as f:
    for line in f:
        triplet_num += 1
        triplet = line.strip().split('\t')
        entities.add(triplet[0])
        entities.add(triplet[2])
        relations.add(triplet[1])

#################
# 测试原本的 578 个实体是否都在第二次过滤后的 KG 中
for entity in entity2id.keys():
    if entity not in entities:
        print(entity)

print(len(entities))
print(len(relations))
print(triplet_num)
#################
        
entities2id = {}
num_of_entities = 578
for entity in entities:
    if entity in entity2id.keys():
        entities2id[entity] = entity2id[entity]
    else:
        entities2id[entity] = str(num_of_entities)
        num_of_entities += 1

num_of_relations = 0
relations2id = {}
for relation in relations:
    relations2id[relation] = str(num_of_relations)
    num_of_relations += 1

with open(kg_path, 'r') as fin:
    with open(kg_final_path, 'w') as fout:
        for line in fin:
            triplet = line.strip().split('\t')
            triplet[0] = entities2id[triplet[0]]
            triplet[1] = relations2id[triplet[1]]
            triplet[2] = entities2id[triplet[2]]
            fout.write('\t'.join(triplet) + '\n')

entities2id_path = 'stage2\stage2\data\Douban\entities2id.txt'
relations2id_path = 'stage2/stage2/data/Douban/relations2id.txt'
with open(entities2id_path, 'w') as f:
    for entity, _id in entities2id.items():
        f.write(entity + '\t' + _id + '\n')

with open(relations2id_path, 'w') as f:
    for relation, _id in relations2id.items():
        f.write(relation + '\t' + _id + '\n')
