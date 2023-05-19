def star(num):
    if num > 5:
        num = 10 - num
    for i in range(5 - num):
        print(' ', end='')
    for i in range(num):
        print('* ', end='')


def star1(num):
    k = 0
    if num > 5:
        num = 10 - num
    for i in range(5 - num):
        print(' ', end='')
    print('*', end='')
    if num > 1:
        k = 2 * (num - 2) + 1
    for i in range(k):
        print(' ', end='')
    if num != 1:
        print('*', end='')


if __name__ == '__main__':
    for i in range(1, 10):
        star(i)
        print()
    for i in range(1, 10):
        star1(i)
        print()
