import threading


def fun():
    while True:
        pass


if __name__ == '__main__':
    t1 = threading.Thread(target=fun)
    t2 = threading.Thread(target=fun)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
