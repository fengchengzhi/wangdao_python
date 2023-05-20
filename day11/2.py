import random


class Loop_Queue:
    def __init__(self, maxsize):
        self.maxsize = maxsize
        self.list = [0] * (maxsize + 1)
        self.maxsize = maxsize + 1
        self.rear = self.front = 0
        self.len = 0

    def is_empty(self):
        if self.rear == self.front:
            return True
        else:
            return False

    def is_full(self):
        if (self.rear + 1) % self.maxsize == self.front:
            return True
        else:
            return False

    def inqueue(self, val):
        if self.is_full():
            print('queue is full')
            return
        self.list[self.rear] = val
        self.rear = (self.rear + 1) % self.maxsize
        print(self.list[self.front:self.rear])
        self.len += 1

    def dequeue(self):
        if self.is_empty():
            print('queue is empty')
            return
        x = self.list[self.front]
        self.front = (self.front + 1) % self.maxsize
        print(self.list[self.front:self.rear])
        self.len -= 1
        return x


if __name__ == '__main__':
    ppp = Loop_Queue(5)
    for i in range(5):
        ppp.inqueue(random.randint(0, 100))
    for i in range(6):
        ppp.dequeue()
