import gzip


def ExtractId2Entity(douban2fb_path):
    entities_set = set()
    with open(douban2fb_path, 'r') as f:
        for i in f.readlines():
            entity = i.strip().split()[1]
            entities_set.add("<http://rdf.freebase.com/ns/{}>".format(entity))
    return entities_set


def ExtractKG2Entity(KG_path):
    entities_set = set()
    with open(KG_path, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            triplet = line.strip().split('\t')
            entities_set.add(triplet[0])
            entities_set.add(triplet[2])
    return entities_set


def ExtractList2Entity(triple_list):
    entities_set = set()
    relation_set = set()
    for triplet in triple_list:
        entities_set.add(triplet[0])
        entities_set.add(triplet[2])
        relation_set.add(triplet[1])
    return entities_set, relation_set


def ExtractFreebase(freebase_path, KG_path, entities_set):
    with gzip.open(freebase_path, 'rb') as f:
        with open(KG_path, 'w', encoding='utf-8') as f_out:
            for line in f:
                line = line.strip()
                triplet = line.decode().split('\t')[:3]
                if triplet[0] in entities_set or triplet[2] in entities_set:
                    f_out.write('\t'.join(triplet) + '\n')


def ExtractFreebase2Step(freebase_path, KG_path, entities_set):
    with gzip.open(freebase_path, 'rb') as f:
        with gzip.open(KG_path, 'wb') as f_out:
            for line in f:
                line = line.strip()
                triplet = line.decode().split('\t')[:3]
                if triplet[0] in entities_set or triplet[2] in entities_set:
                    f_out.write(('\t'.join(triplet) + '\n').encode())


if __name__ == '__main__':
    entities = ExtractId2Entity('../data/douban2fb.txt')
    ExtractFreebase('../data/freebase_douban.gz', '../data/extract_entity1.txt', entities)