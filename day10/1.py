class Test:
    instance = None

    @staticmethod
    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self, name):
        self.name = name


if __name__ == '__main__':
    t1 = Test('111')
    print(t1)
    print(t1.name)
    t2 = Test('222')
    print(t2)
    print(t2.name)
