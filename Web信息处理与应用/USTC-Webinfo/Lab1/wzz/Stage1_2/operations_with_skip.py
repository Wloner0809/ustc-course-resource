from skip_list import Skip_revert_list
from typing import Tuple
import json


def AND_NOT(T1: Tuple, T2: Tuple) -> list:
    ret = []
    L1 = T1[0]
    L2 = T2[0]
    Skip_1 = T1[1]
    Skip_2 = T2[1]
    if not L1 or not L2:
        print("The operand 'OR' lacks parameter!\n".center(output_len))
        error = True
    else:
        index1 = 0
        index2 = 0
        len_1 = len(L1) 
        len_2 = len(L2)
        interval_1 = int((len(L1)) ** 0.5)
        interval_2 = int((len(L2)) ** 0.5)
        while index1 < len(L1) and index2 < len(L2):
            while index1 % interval_1 == 0 and index1 < len_1 - interval_1:     #index1有跳表指针
                if L1[index1] == L2[index2] and Skip_1[index1 // interval_1 + 1][0] == L2[index2]:
                    index1 += interval_1
                    index2 += 1
                elif L1[index1] < L2[index2] and Skip_1[index1 // interval_1 + 1][0] < L2[index2]:
                    ret.extend(L1[index1 : index1 + interval_1])
                    index1 += interval_1
                else:
                    break           #跳表失败
            while index2 % interval_2 == 0 and index2 < len_2 - interval_2:     #index2有跳表指针
                if L2[index2] == L1[index1] and Skip_2[index2 // interval_2 + 1][0] == L1[index1]:
                    index2 += interval_2
                    index1 += 1
                elif L2[index2] < L1[index1] and Skip_2[index2 // interval_2 + 1][0] < L1[index1]:
                    index2 += interval_2
                else:
                    break           #跳表失败
            
            if L1[index1] == L2[index2]:
                index1 += 1
                index2 += 1
            elif L1[index1] < L2[index2]:
                ret.append(L1[index1])
                index1 += 1
            else:
                index2 += 1

        if index1 < len(L1):
            ret.extend(L1[index1:])
    return ret


def OR(T1: Tuple, T2: Tuple) -> list:
    ret = []
    L1 = T1[0]
    L2 = T2[0]
    Skip_1 = T1[1]
    Skip_2 = T2[1]
    if not L1 or not L2:
        print("The operand 'OR' lacks parameter!\n".center(output_len))
        error = True
    else:
        index1 = 0
        index2 = 0
        len_1 = len(L1) 
        len_2 = len(L2)
        interval_1 = int((len(L1)) ** 0.5)
        interval_2 = int((len(L2)) ** 0.5)
        while index1 < len(L1) and index2 < len(L2):
            while index1 % interval_1 == 0 and index1 < len_1 - interval_1:     #index1有跳表指针
                if L1[index1] == L2[index2] and Skip_1[index1 // interval_1 + 1][0] == L2[index2]:
                    ret.extend(L1[index1 : index1 + interval_1])
                    index1 += interval_1
                    index2 += 1
                elif L1[index1] < L2[index2] and Skip_1[index1 // interval_1 + 1][0] < L2[index2]:
                    ret.extend(L1[index1 : index1 + interval_1])
                    index1 += interval_1
                else:
                    break           #跳表失败
            while index2 % interval_2 == 0 and index2 < len_2 - interval_2:     #index2有跳表指针
                if L2[index2] == L1[index1] and Skip_2[index2 // interval_2 + 1][0] == L1[index1]:
                    ret.extend(L2[index2 : index2 + interval_2])
                    index2 += interval_2
                    index1 += 1
                elif L2[index2] < L1[index1] and Skip_2[index2 // interval_2 + 1][0] < L1[index1]:
                    ret.extend(L2[index2 : index2 + interval_2])
                    index2 += interval_2
                else:
                    break           #跳表失败
            
            if L1[index1] == L2[index2]:
                ret.append(L1[index1])
                index1 += 1
                index2 += 1
            elif L1[index1] < L2[index2]:
                ret.append(L1[index1])
                index1 += 1
            else:
                ret.append(L2[index2])
                index2 += 1

        if index1 < len(L1):
            ret.extend(L1[index1:])
        if index2 < len(L2):
            ret.extend(L2[index2:])
    return ret

def AND(T1: Tuple, T2: Tuple) -> list:
    ret = []
    L1 = T1[0]
    L2 = T2[0]
    Skip_1 = T1[1]
    Skip_2 = T2[1]
    if not L1 or not L2:
        print("The operand 'AND' lacks parameter!")
    else:
        index1 = 0
        index2 = 0
        len_1 = len(L1) 
        len_2 = len(L2)
        interval_1 = int((len(L1)) ** 0.5)
        interval_2 = int((len(L2)) ** 0.5)
        while index1 < len_1 and index2 < len_2:
            #try_skip
            while index1 % interval_1 == 0 and index1 < len_1 - interval_1:     #index1有跳表指针
                if L1[index1] < L2[index2] and Skip_1[index1 // interval_1 + 1][0] < L2[index2]:
                    index1 = Skip_1[index1 // interval_1][1]
                else:
                    break
            while index2 % interval_2 == 0 and index2 < len_2 - interval_2:     #index2有跳表指针
                if L2[index2] < L1[index1] and Skip_2[index2 // interval_2 + 1][0] < L1[index1]:
                    index2 = Skip_2[index2 // interval_2][1]
                else:
                    break

            if L1[index1] == L2[index2]:
                ret.append(L1[index1])
                index1 += 1
                index2 += 1
            elif L1[index1] < L2[index2]:
                index1 += 1
            else:
                index2 += 1
    return ret


if __name__ == "__main__":
    with open(r"D:\web_lab\WebInfo\Lab1\wy\Stage1_2\Result\Book_keyword.json","r",encoding="UTF-8") as fin:
        participle_dict = json.load(fin)
    skip = Skip_revert_list(participle_dict)
    print( AND((skip.reverted_dict["一部"],skip.skip_dict["一部"]) , (skip.reverted_dict["动人"],skip.skip_dict["动人"])) )
    print("\n")
    print( OR ((skip.reverted_dict["挪威"],skip.skip_dict["挪威"]) , (skip.reverted_dict["森林"],skip.skip_dict["森林"])) )
    print("\n")
    print( AND_NOT ((skip.reverted_dict["一部"],skip.skip_dict["一部"]) , (skip.reverted_dict["动人"],skip.skip_dict["动人"])) )