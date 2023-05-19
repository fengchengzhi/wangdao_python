from collections.abc import Iterable


class Mylist:
    def __init__(self):
        self.container = []

    def add(self, num):
        self.container.append(num)

    def __iter__(self):
        my_iterator = MyIterator(self)
        return my_iterator


class MyIterator:
    def __init__(self, mylist: Mylist):
        self.mylist = mylist
        self.current = 0

    def __next__(self):
        current = self.current
        self.current += 1
        if current < len(self.mylist.container):
            return self.mylist.container[current]
        else:
            raise StopIteration

    def __iter__(self):
        return self


if __name__ == '__main__':
    li = Mylist()
    for i in range(5):
        li.add(i * 2)
    print(li.container)
    for i in li:
        print(i, end=' ')
