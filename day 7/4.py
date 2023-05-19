def majority(l1):
    dict1 = {}
    for i in l1:
        a = dict1.get(i, -1)
        if a == -1:
            dict1[i] = 1
        else:
            dict1[i] += 1
    num = 0
    key = 0
    for j in dict1:
        if num < dict1[j]:
            key = j
            num = dict1[j]
    print(dict1)
    return key


if __name__ == '__main__':
    a='3125165486531654654846531'
    list1 = list(a)
    print(majority(list1))
