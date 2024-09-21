import json


def decompress(compress_path, word_list_path):
    with open(compress_path, 'rb') as f_compress:
        contents_bytes = f_compress.read()
        contents_list = []
        content_list = []
        for byte in contents_bytes:
            if byte >> 7 == 0:
                content_list.append(byte)
            else:
                content_list.append(byte & 0x7f)
                contents_list.append(content_list)
                del content_list
                content_list = []  # 不能用 content.clear()

    with open(word_list_path, 'r', encoding='UTF-8') as f_word:
        word_list = f_word.readlines()

    index = 0
    inverted_table = {}
    id_list = []
    content_index = 0
    while index < len(word_list):
        word_and_num = word_list[index].strip().split('%')
        if len(word_and_num) != 2:
            print(word_and_num)
            break
        word = word_and_num[0]
        num = int(word_and_num[1])
        for i in range(num):
            id_bytes = contents_list[content_index + i]
            id_ = 0
            for j in range(0, len(id_bytes)):
                id_ += id_bytes[len(id_bytes) - 1 - j] << j * 7
            id_ += id_list[i - 1] if id_list else 0
            id_list.append(id_)
        inverted_table[word] = id_list
        content_index += num
        index += 1
        del id_list
        id_list = []
    return inverted_table


_dict = decompress("../../wzz/Stage1_2/data/Movie_reverted_dict_compressed.bin",
                   "../../wzz/Stage1_2/data/Movie_vocabulary.txt")
with open('Movie_reverted_dict.json', "w", encoding="UTF-8") as f:
    json.dump(_dict, f, indent=4, ensure_ascii=False)
