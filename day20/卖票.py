import threading

vote = 1000000


def windows1():
    global vote
    num = 0
    while True:
        mutex.acquire()
        if vote > 0:
            vote -= 1
            num += 1
        mutex.release()
        if vote <= 0:
            break
    print(f'I sold {num} votes')


def windows2():
    global vote
    num = 0
    while True:
        mutex.acquire()
        if vote > 0:
            vote -= 1
            num += 1
        mutex.release()
        if vote <= 0:
            break
    print(f'I sold {num} votes')


def windows3():
    global vote
    num = 0
    while True:
        mutex.acquire()
        if vote > 0:
            vote -= 1
            num += 1
        mutex.release()
        if vote <= 0:
            break
    print(f'I sold {num} votes')


if __name__ == '__main__':
    mutex = threading.Lock()
    t1 = threading.Thread(target=windows1)
    t2 = threading.Thread(target=windows2)
    t3 = threading.Thread(target=windows3)
    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()
