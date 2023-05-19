from multiprocessing import Process
import time


def proc(num):
    while True:
        time.sleep(1)
        print(num)
        num += 1


if __name__ == '__main__':
    po = Process(target=proc, args=(1,))
    po.start()
    print('I am father')
