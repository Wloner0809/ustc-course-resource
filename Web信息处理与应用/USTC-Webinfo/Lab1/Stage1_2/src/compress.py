import json


def compress(index_list) -> bytes:
    count = 0
    vb_arr = []  # 可变长度编码对应的列表（最后转换成bytes类）
    prev = len(index_list) - 2

    for i in range(len(index_list) - 1, 0, -1):  # 用文档间距替代id
        index_list[i] = index_list[i] - index_list[prev]
        prev -= 1

    for i in range(0, len(index_list)):  # index_list:若干个长的id
        reverted_arr = []
        while index_list[i] >= 128:
            mod = index_list[i] % 128
            reverted_arr.append(mod)
            index_list[i] = index_list[i] >> 7
        if index_list[i] > 0:
            reverted_arr.append(index_list[i])
        reverted_arr[0] = int(reverted_arr[0]) + 128
        for j in range(len(reverted_arr) - 1, -1, -1):  # 倒着遍历
            vb_arr.append(reverted_arr[j])
        pass
    result = bytes(vb_arr)
    return result


if __name__ == "__main__":
    with open("data/Movie_reverted_dict.json", "r", encoding="UTF-8") as f_in:
        reverted_dict = json.load(f_in)

    with open("data/Movie_reverted_dict_compressed.bin", "wb") as f_bin:
        with open("data/Movie_vocabulary.txt", "w", encoding="UTF-8") as f_txt:
            for key in reverted_dict:
                f_txt.write(key + "%" + str(len(reverted_dict[key])) + "\n")
                reverted_dict[key] = compress(reverted_dict[key])
                f_bin.write(reverted_dict[key])
