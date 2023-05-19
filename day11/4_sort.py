import random


class Sort:
    def __init__(self, a_len, a_max):
        self.a_len = a_len
        self.a_max = a_max
        self.arr = []
        self.temp = [] * a_len

    # 初始化
    def init(self):
        for i in range(self.a_len):
            self.arr.append(random.randint(0, self.a_max))
        print(self.arr)

    # 冒泡
    def bubble(self):
        for i in range(self.a_len, 1, -1):
            for j in range(i - 1):
                if self.arr[j + 1] < self.arr[j]:
                    self.arr[j + 1], self.arr[j] = self.arr[j], self.arr[j + 1]

    # 测试
    def my_sort(self, method, *args, **kwargs):
        self.init()
        method(*args, **kwargs)
        print(self.arr)

    # 选择
    def select(self):
        for i in range(0, self.a_len - 1):
            for j in range(i + 1, self.a_len):
                if self.arr[i] > self.arr[j]:
                    self.arr[i], self.arr[j] = self.arr[j], self.arr[i]

    # 插入
    def insert_s(self):
        for i in range(1, self.a_len):
            val = self.arr[i]
            for j in range(i, -1, -1):
                if self.arr[j - 1] > val:
                    self.arr[j] = self.arr[j - 1]
                else:
                    break
            self.arr[j] = val

    # 希尔
    def shell_s(self):
        gap = self.a_len >> 1
        while gap:
            for i in range(gap, self.a_len, gap):
                val = self.arr[i]
                for j in range(i, -1, -gap):
                    if self.arr[j - gap] > val:
                        self.arr[j] = self.arr[j - gap]
                    else:
                        break
                self.arr[j] = val
            gap >>= 1

    # 快排分割
    def partition(self, left, right):
        j = left
        for i in range(left, right):
            if self.arr[i] < self.arr[right]:
                self.arr[j], self.arr[i] = self.arr[i], self.arr[j]
                j += 1
        self.arr[j], self.arr[right] = self.arr[right], self.arr[j]
        return j

    # 快排
    def quick_s(self, left, right):
        if left > right:
            return
        pivot = self.partition(left, right)
        self.quick_s(left, pivot - 1)
        self.quick_s(pivot + 1, right)

    # 调整大根堆
    def adjust_heap(self, dad, arr_len):
        while dad <= (arr_len - 1) // 2:
            child = 2 * dad + 1
            if child + 1 <= arr_len and self.arr[child] < self.arr[child + 1]:
                child += 1
            if self.arr[dad] < self.arr[child]:
                self.arr[dad], self.arr[child] = self.arr[child], self.arr[dad]
            else:
                break
            dad = child

    # 堆排
    def heap(self):
        arr_len = self.a_len - 1
        for i in range((self.a_len - 1) // 2, -1, -1):
            self.adjust_heap(i, arr_len)
        self.arr[arr_len], self.arr[0] = self.arr[0], self.arr[arr_len]
        arr_len -= 1
        for i in range(self.a_len - 1):
            self.adjust_heap(0, arr_len)
            self.arr[arr_len], self.arr[0] = self.arr[0], self.arr[arr_len]
            arr_len -= 1

    # 合并有序数组
    def merge(self, left, mid, right):
        i = k = left
        j = mid + 1
        self.temp[left:right + 1] = self.arr[left:right + 1]
        while i <= mid and j <= right:
            if self.temp[i] <= self.temp[j]:
                self.arr[k] = self.temp[i]
                k += 1
                i += 1
            else:
                self.arr[k] = self.temp[j]
                k += 1
                j += 1
        while i <= mid:
            self.arr[k] = self.temp[i]
            k += 1
            i += 1
        while j <= right:
            self.arr[k] = self.temp[j]
            k += 1
            j += 1

    # 归并
    def merge_sort(self, left, right):
        if right <= left:
            return
        mid = (left + right) // 2
        self.merge_sort(left, mid)
        self.merge_sort(mid + 1, right)
        self.merge(left, mid, right)


if __name__ == '__main__':
    a = Sort(20, 100)
    a.my_sort(a.merge_sort, 0, 19)
