from typing import Dict, List
import gzip


class Filter:
    def __init__(self, KG_path, entities_min, entities_max, relation_min, mode='first'):
        self.entities_min = entities_min
        self.entities_max = entities_max
        self.relation_min = relation_min
        self.KG_path = KG_path
        self.mode = mode
        self.triple_list = self.__get_triple_set()
        self.entities_count, self.relation_count = self.__get_count()

    def __get_triple_set(self) -> List:
        # 从三元组文件中读取三元组
        if self.mode == 'first':
            with open(self.KG_path, 'r', encoding='utf-8') as f:
                triple_list = [line.strip().split('\t') for line in f.readlines()]
            assert triple_list
            return triple_list
        else:
            with gzip.open(self.KG_path, 'rb') as f:
                triple_list = [line.strip().decode().strip().split('\t') for line in f.readlines()]
            assert triple_list
            return triple_list

    def __get_count(self) -> (Dict, Dict):
        entities_count = {}
        relation_count = {}
        for triplet in self.triple_list:
            entities_count[triplet[0]] = entities_count.get(triplet[0], 0) + 1
            entities_count[triplet[2]] = entities_count.get(triplet[2], 0) + 1
            relation_count[triplet[1]] = relation_count.get(triplet[1], 0) + 1
        return entities_count, relation_count

    def __filter_prefix(self):
        prefix = '<http://rdf.freebase.com/ns/'
        triple_list_filter_prefix = [triplet for triplet in self.triple_list if
                                     triplet[0].startswith(prefix) and triplet[2].startswith(prefix)]
        return triple_list_filter_prefix

    def __filter_entities(self):
        triple_list_filter_entities = []
        for triplet in self.triple_list:
            if (self.entities_min <= self.entities_count[triplet[0]] <= self.entities_max) and (
                    self.entities_min <= self.entities_count[triplet[2]] <= self.entities_max):
                triple_list_filter_entities.append(triplet)
        return triple_list_filter_entities

    def __filter_relations(self):
        triple_filter_relation = [triplet for triplet in self.triple_list if
                                  self.relation_count[triplet[1]] >= self.relation_min]
        return triple_filter_relation

    def filter(self):
        self.triple_list = self.__filter_prefix()
        self.triple_list = self.__filter_relations()
        self.triple_list = self.__filter_entities()
        return self.triple_list

    def save(self, save_path):
        with open(save_path, "w", encoding='utf-8') as f:
            for triplet in self.triple_list:
                f.write('\t'.join(triplet) + '\n')
