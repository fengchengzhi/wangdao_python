def sum():
    result = 0
    for i in range(100):
        if i % 2 == 0:
            i += 1
            continue
        else:
            result += i
    return result


if __name__ == '__main__':
    num = sum()
    print(num)
