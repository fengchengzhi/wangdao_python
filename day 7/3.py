def common(a, b):
    result = []
    for i in a:
        for j in b:
            if j > i:
                break
            elif i == j:
                result.append(j)
    return result


if __name__ == '__main__':
    list1 = [1, 2, 3, 4, 6, 8, 9]
    list2 = [2, 3, 4, 5, 7, 9]
    print(common(list1, list2))
