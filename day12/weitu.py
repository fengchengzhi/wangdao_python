import random


def init(a_max, a_len):
    arr = []
    for i in range(a_len):
        arr.append(random.randint(0, a_max))
    print(arr)
    return arr


def bit_map(arr: list):
    j = 0
    a_len = len(arr)
    i = 0
    while i < a_len:
        if 1 << arr[i] & j:
            arr.pop(i)
            i -= 1
            a_len -= 1
        else:
            j += 1 << arr[i]
        i += 1
    print(arr)


a = init(10, 20)
bit_map(a)
