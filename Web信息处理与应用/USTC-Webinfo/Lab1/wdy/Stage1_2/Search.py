from typing import AnyStr, List, Tuple, Dict
import json
from colorama import Fore


class BooleanMatch:
    def __init__(self):
        self.query = ""
        self.query_list = []
        self.query_cache_list = []
        self.mode = ""
        self.error = False
        self.info = {}  # info of the mode (Stage1_1)
        self.reverted_dict = {}  # inverted table of the mode (Stage1_2)
        self.skip_list = {}  # skip list of the mode (Stage1_2)
        self.pre_sort_ids = ()

        # Load data
        print(Fore.BLUE + '*' * 22 + " Douban Searching Engine " + '*' * 23)
        print(Fore.RED + '*' * 12 + " LOADING DATA! Please wait for a few seconds! " + '*' * 12)
        self.book_info_path = '../../Stage1_1/Result/Book_info.json'
        self.movie_info_path = '../../Stage1_1/Result/Movie_info.json'
        self.book_reverted_dict_compress_path = '../../Stage1_2/Dataset/Book_reverted_dict_compressed.bin'
        self.book_vocabulary = '../../Stage1_2/Dataset/Book_vocabulary.txt'
        self.movie_reverted_dict_compress_path = '../../Stage1_2/Dataset/Movie_reverted_dict_compressed.bin'
        self.movie_vocabulary = '../../Stage1_2/Dataset/Movie_vocabulary.txt'

        with open(self.book_info_path, 'r', encoding="utf-8") as f_book_info:
            self.book_info = json.load(f_book_info)

        with open(self.movie_info_path, 'r', encoding="utf-8") as f_movie_info:
            self.movie_info = json.load(f_movie_info)

        self.book_reverted_dict = self.decompress(self.book_reverted_dict_compress_path, self.book_vocabulary)
        self.movie_reverted_dict = self.decompress(self.movie_reverted_dict_compress_path, self.movie_vocabulary)

        print(Fore.BLUE + '*' * 12 + " Initialization completed! Start you travel! " + '*' * 13 + '\n')

    def decompress(self, compress_path, word_list_path) -> Dict:
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
                self.error = True
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

    def message(self, _id: int):
        if self.mode == 'book':
            show_id = str(_id) + ' ' * (17 - len(str(_id)))
            show_author = "author: " + self.book_info[str(_id)]["author"]
            show_author = show_author + ' ' * (30 - len(show_author)) if len(show_author) < 30 else ' '
            show_content = "content: " + self.book_info[str(_id)]["content introduction"]
            print(Fore.GREEN + show_id, end='')
            print(Fore.BLACK + show_author, end='')
            print(Fore.BLACK + show_content)
        else:
            show_id = str(_id) + ' ' * (17 - len(str(_id)))
            show_name = "movie name: " + self.movie_info[str(_id)]["name"]
            show_name = show_name + ' ' * (40 - len(show_name)) if len(show_name) < 40 else ' '
            show_director = "director: " + '、'.join(self.movie_info[str(_id)]["director"])
            show_director = show_director + ' ' * (30 - len(show_director)) if len(show_director) < 30 else ' '
            show_content = "content: " + self.movie_info[str(_id)]['intro']
            print(Fore.GREEN + show_id, end='')
            print(Fore.BLACK + show_name, end='')
            print(Fore.BLACK + show_director, end='')
            print(Fore.BLACK + show_content)

    def SplitQuery(self) -> List:
        self.query = self.query.strip()
        self.query = self.query.replace('（', '(').replace('）', ')')
        self.query = self.query.replace('(', ' ( ').replace(')', ' ) ')
        self.query = self.query.upper()
        self.query = self.query.replace('AND', ' AND ').replace('OR', ' OR ').replace('NOT', ' NOT ')
        self.query = self.query.replace('和', ' AND ').replace('且', ' OR ').replace('非', ' NOT ')
        self.query = self.query.replace('&',' AND ').replace('|',' OR ').replace('!',' NOT ')
        return self.query.split()

    def FindCorrespondBracket(self, index: int) -> int:
        i = index + 1
        flag = 0
        while i < len(self.query_list) and not self.error:
            if flag < 0:
                print("The right bracket overabundant!")
                self.error = True
            elif self.query_list[i] == ')':
                if flag == 0:
                    return i
                else:
                    flag -= 1
            elif self.query_list[i] == '(':
                flag += 1
            i += 1
        print("Lack of right bracket!")
        self.error = True
        return -1

    def CreateSkipList(self, L: List) -> List:
        if len(L) == 0:
            self.error = True
            return []
        if not self.error:
            interval = int(len(L) ** 0.5)
            skip_list = [[L[0], 0 if len(L) == 1 else interval, 0]]  # avoid len(L) == 1
            for i in range(interval, len(L) - interval, interval):
                skip_list.append([L[i], i + interval, i])
            last = len(skip_list) * interval
            if last < len(L) - 1:
                skip_list.append([(L[last]), len(L) - 1, last])
            return skip_list

    def BooleanSearch(self, query: AnyStr, mode: AnyStr) -> bool:
        self.query = query
        self.mode = mode
        self.query_list = self.SplitQuery()
        self.info = self.book_info if mode == 'book' else self.movie_info
        self.reverted_dict = self.book_reverted_dict if mode == 'book' else self.movie_reverted_dict
        # self.skip_list = self.book_skip_list if mode == 'book' else self.movie_skip_list
        pre_sort_id_list = list(self.info.keys())
        pre_sort_id_list.sort()
        self.pre_sort_ids = (pre_sort_id_list, self.CreateSkipList(pre_sort_id_list))

        ret, ret_skip_list = self.BracketOperation(self.query_list)
        if len(ret) == 0:
            print(Fore.RED + "Sorry! But there are no results you want here.")
            # not find doesn't mean error, but doesn't need to output
        elif not self.error:
            print(Fore.BLUE + '*' * 50)
            for _id in ret:
                self.message(_id)
            print(Fore.BLUE + '*' * 50)

        return self.error

    def BracketOperation(self, query_list: List) -> Tuple:
        if not query_list:
            return [], []
        ret = []
        index = 0
        while index < len(query_list):
            item = query_list[index]
            if not self.error:
                if item == '(':
                    l_bracket = index
                    r_bracket = self.FindCorrespondBracket(l_bracket)
                    if not self.error:
                        ret.append(self.BracketOperation(query_list[l_bracket + 1: r_bracket]))
                        index = r_bracket + 1
                    else:
                        index += 1
                elif item == 'AND' or item == 'OR' or item == 'NOT':
                    ret.append(item)
                    index += 1
                else:
                    item_id_list = self.reverted_dict[item] if item in self.reverted_dict.keys() else []
                    item_skip_list = self.CreateSkipList(item_id_list)
                    item_id_list_and_skip_list = (item_id_list, item_skip_list)
                    ret.append(item_id_list_and_skip_list)
                    index += 1
            else:
                break
        logic_ret = self.LogicOperation(ret)

        return logic_ret

    def LogicOperation(self, ret: List) -> Tuple:
        if 'OR' in ret:
            or_list = []
            for loc, val in enumerate(ret):
                if val == 'OR':
                    or_list.append(loc)
            last_or_index = or_list[-1]
            return self.OR(self.LogicOperation(ret[: last_or_index]), self.LogicOperation(ret[last_or_index + 1:]))
        elif 'AND' in ret:
            and_list = []
            for loc, val in enumerate(ret):
                if val == 'AND':
                    and_list.append(loc)
            last_and_index = and_list[-1]
            if ret[last_and_index + 1] == 'NOT':
                if ret[last_and_index + 2] != 'NOT':
                    return self.AND_NOT(self.LogicOperation(ret[: last_and_index]),
                                        self.LogicOperation(ret[last_and_index + 2:]))
            return self.AND(self.LogicOperation(ret[: last_and_index]),
                            self.LogicOperation(ret[last_and_index + 1:]))
        elif 'NOT' in ret:
            first_not_index = ret.index('NOT')
            if ret[first_not_index + 1] == 'NOT':
                if ret[first_not_index + 2] != 'NOT':
                    return self.LogicOperation(ret[first_not_index + 2:])
            else:
                return self.NOT(self.LogicOperation(ret[first_not_index + 1:]))
        else:
            if not self.error and len(ret) == 0:
                print(Fore.RED + "Lack of some parameters")
                self.error = True
            elif not self.error and len(ret) > 1:
                print(Fore.RED + "There are some unexpected parameters")
                self.error = True
            if not self.error:
                return ret[0]
            else:
                return [], []

    def OR(self, T1: Tuple, T2: Tuple) -> Tuple:
        ret = []
        L1_id_list = T1[0]
        L2_id_list = T2[0]
        L1_skip_list = T1[1]
        L2_skip_list = T2[1]
        if not L1_id_list or not L2_id_list:
            print(Fore.RED + "The operand 'OR' lacks parameter!")
            self.error = True
        else:
            index1 = 0
            index2 = 0
            len_1 = len(L1_id_list)
            len_2 = len(L2_id_list)
            interval_1 = int((len(L1_id_list)) ** 0.5)
            interval_2 = int((len(L2_id_list)) ** 0.5)
            while index1 < len(L1_id_list) and index2 < len(L2_id_list):
                while index1 % interval_1 == 0 and index1 < len_1 - interval_1:  # index1 should skip
                    if L1_id_list[index1] == L2_id_list[index2] and L1_id_list[L1_skip_list[index1 // interval_1][1]] == \
                            L2_id_list[index2]:
                        ret.extend(L1_id_list[index1: index1 + interval_1])
                        index1 += interval_1
                        index2 += 1
                    elif L1_id_list[index1] < L2_id_list[index2] and L1_id_list[L1_skip_list[index1 // interval_1][1]] < \
                            L2_id_list[index2]:
                        ret.extend(L1_id_list[index1: index1 + interval_1])
                        index1 += interval_1
                    else:
                        break  # fail skip
                while index2 % interval_2 == 0 and index2 < len_2 - interval_2:  # index2 should skip
                    if L2_id_list[index2] == L1_id_list[index1] and L2_id_list[L2_skip_list[index2 // interval_2][1]] == \
                            L1_id_list[index1]:
                        ret.extend(L2_id_list[index2: index2 + interval_2])
                        index2 += interval_2
                        index1 += 1
                    elif L2_id_list[index2] < L1_id_list[index1] and L2_id_list[L2_skip_list[index2 // interval_2][1]] < \
                            L1_id_list[index1]:
                        ret.extend(L2_id_list[index2: index2 + interval_2])
                        index2 += interval_2
                    else:
                        break  # fail skip

                if L1_id_list[index1] == L2_id_list[index2]:
                    ret.append(L1_id_list[index1])
                    index1 += 1
                    index2 += 1
                elif L1_id_list[index1] < L2_id_list[index2]:
                    ret.append(L1_id_list[index1])
                    index1 += 1
                else:
                    ret.append(L2_id_list[index2])
                    index2 += 1

            if index1 < len(L1_id_list):
                ret.extend(L1_id_list[index1:])
            if index2 < len(L2_id_list):
                ret.extend(L2_id_list[index2:])

        return ret, self.CreateSkipList(ret)

    def AND(self, T1: Tuple, T2: Tuple) -> Tuple:
        ret = []
        L1_id_list = T1[0]
        L1_skip_list = T1[1]
        L2_id_list = T2[0]
        L2_skip_list = T2[1]
        if not L1_id_list or not L2_id_list:
            print(Fore.RED + "The operand 'AND' lacks parameter!")
            self.error = True
        if not self.error:
            index1 = 0
            index2 = 0
            len_1 = len(L1_id_list)
            len_2 = len(L2_id_list)
            interval_1 = int((len(L1_id_list)) ** 0.5)
            interval_2 = int((len(L2_id_list)) ** 0.5)
            while index1 < len_1 and index2 < len_2:
                # try_skip
                while index1 % interval_1 == 0 and index1 < len_1 - interval_1:  # index1 should skip
                    if L1_id_list[index1] < L2_id_list[index2] and L1_id_list[L1_skip_list[index1 // interval_1][1]] < \
                            L2_id_list[index2]:
                        index1 = L1_skip_list[index1 // interval_1][1]
                    else:
                        break
                while index2 % interval_2 == 0 and index2 < len_2 - interval_2:  # index2 should skip
                    if L2_id_list[index2] < L1_id_list[index1] and L2_id_list[L2_skip_list[index2 // interval_2][1]] < \
                            L1_id_list[index1]:
                        index2 = L2_skip_list[index2 // interval_2][1]
                    else:
                        break

                if L1_id_list[index1] == L2_id_list[index2]:
                    ret.append(L1_id_list[index1])
                    index1 += 1
                    index2 += 1
                elif L1_id_list[index1] < L2_id_list[index2]:
                    index1 += 1
                else:
                    index2 += 1

        return ret, self.CreateSkipList(ret)

    def AND_NOT(self, T1: Tuple, T2: Tuple) -> Tuple:
        ret = []
        L1_id_list = T1[0]
        L2_id_list = T2[0]
        L1_skip_list = T1[1]
        L2_skip_list = T2[1]
        if not L1_id_list or not L2_id_list:
            print(Fore.RED + "The operand 'NOT' lacks parameter!")
            self.error = True
        else:
            index1 = 0
            index2 = 0
            len_1 = len(L1_id_list)
            len_2 = len(L2_id_list)
            interval_1 = int((len(L1_id_list)) ** 0.5)
            interval_2 = int((len(L2_id_list)) ** 0.5)
            while index1 < len(L1_id_list) and index2 < len(L2_id_list):
                while index1 % interval_1 == 0 and index1 < len_1 - interval_1:  # index1 should skip
                    if L1_id_list[index1] == L2_id_list[index2] and L1_id_list[L1_skip_list[index1 // interval_1][1]] == \
                            L2_id_list[index2]:
                        ret.extend(L1_id_list[index1: index1 + interval_1])
                        index1 += interval_1
                        index2 += 1
                    elif L1_id_list[index1] < L2_id_list[index2] and L1_id_list[L1_skip_list[index1 // interval_1][1]] < \
                            L2_id_list[index2]:
                        ret.extend(L1_id_list[index1: index1 + interval_1])
                        index1 += interval_1
                    else:
                        break  # fail skip
                while index2 % interval_2 == 0 and index2 < len_2 - interval_2:  # index2 should skip
                    if L2_id_list[index2] == L1_id_list[index1] and L2_id_list[L2_skip_list[index2 // interval_2][1]] == \
                            L1_id_list[index1]:
                        ret.extend(L2_id_list[index2: index2 + interval_2])
                        index2 += interval_2
                        index1 += 1
                    elif L2_id_list[index2] < L1_id_list[index1] and L2_id_list[L2_skip_list[index2 // interval_2][1]] < \
                            L1_id_list[index1]:
                        ret.extend(L2_id_list[index2: index2 + interval_2])
                        index2 += interval_2
                    else:
                        break  # fail skip

                if L1_id_list[index1] == L2_id_list[index2]:
                    index1 += 1
                    index2 += 1
                elif L1_id_list[index1] < L2_id_list[index2]:
                    ret.append(L1_id_list[index1])
                    index1 += 1
                else:
                    index2 += 1

            if index1 < len(L1_id_list):
                ret.extend(L1_id_list[index1:])

        return ret, self.CreateSkipList(ret)

    def NOT(self, T: Tuple) -> Tuple:
        return self.AND_NOT(self.pre_sort_ids, T)


if __name__ == '__main__':
    bm = BooleanMatch()
    while True:
        while True:
            user_mode = input(Fore.BLACK +
                              "Please input which mode you'll search: " + Fore.GREEN + "book / movie? ")
            if user_mode == 'book' or user_mode == 'movie':
                break
            else:
                print(Fore.RED + "Some error! Please be care that you can only choose 'book' or 'movie'!")

        user_query = input(Fore.BLACK + "Please input the sequence you'll search: ")

        error = bm.BooleanSearch(user_query, user_mode)

        if error:
            next_choice = input(Fore.BLACK + "Maybe search for something else?" + Fore.GREEN + "[Y/n] ")
        else:
            next_choice = input(Fore.BLACK + "Continue?" + Fore.GREEN + "[Y/n] ")

        if next_choice == 'n':
            print(
                Fore.BLUE + "Thank you for using this searching engine! Welcome your next travel!")
            break

# 一场 AND not NOt 谋杀案
# 一部 and 动人心弦
# 挪威And 森林
# 功夫 and not 喜剧
