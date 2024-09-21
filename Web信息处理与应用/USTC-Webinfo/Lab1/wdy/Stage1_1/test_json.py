import json

save_path = '../Result/Book_info.json'
with open(save_path, 'r', encoding='UTF-8') as f:
    json_data = json.load(f)

tag_path = '../Dataset/Tag/Book_tag.csv'
with open(tag_path, 'r', encoding='UTF-8') as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip('\n')
        index = line.find(',')
        if index != -1:
            movie_id = line[0:index]
            tag = line[index + 1:]
            print(movie_id, ' ', tag)
        if movie_id not in json_data.keys():
            continue
        json_data[movie_id]['tag'] = tag.strip('"').split(',')

save_path_1 = '../Result/Book_info1.json'
with open(save_path_1, 'w', encoding='UTF-8') as f:
    json.dump(json_data, f, indent=4, ensure_ascii=False)
