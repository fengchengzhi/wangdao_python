try:
    x = int(input())
    print(x + 1)
except ValueError as e:
    print('wrong')
finally:
    print('fff')
