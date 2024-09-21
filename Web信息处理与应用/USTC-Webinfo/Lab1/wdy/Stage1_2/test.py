def SplitQuery(query):
    query = query.strip()
    query = query.replace('（', '(').replace('）', ')')
    query = query.replace('(', ' ( ').replace(')', ' ) ')
    query = query.upper()
    query = query.replace('AND', ' AND ').replace('OR', ' OR ').replace('NOT', ' NOT ')
    query_list = query.split()
    return query_list


def FindCorrespondBracket(query_list, index: int):
    i = index + 1
    flag = 0
    error = False
    while i < len(query_list):
        if flag < 0:
            error = True
        elif query_list[i] == ')':
            if flag == 0:
                return i, error
            else:
                flag -= 1
        elif query_list[i] == '(':
            flag += 1
        i += 1
    error = True
    return -1, error


# 是否 and 地球 NOt   （Aor微软）
query = input("Please input a str:\n")
ret = SplitQuery(query)
print(ret)

co_index, error = FindCorrespondBracket(ret, 4)
print(co_index, error)