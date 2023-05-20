class Person:
    def __init__(self, name, age, height, weight):
        self.name = name
        self.age = age
        self.height = height
        self.weight = weight

    def run(self):
        self.weight -= 0.5
        print('体重减少了0.5kg')

    def eat(self):
        self.weight += 0.5
        print('体重增加了0.5kg')

    def __str__(self):
        return f'姓名{self.name},年龄{str(self.age)},身高{str(self.height)},体重{str(self.weight)}'

xiaoming=Person('xiaoming',18,175,65)
print(xiaoming)
xiaoming.run()
print(xiaoming)
xiaoming.run()
print(xiaoming)
xiaoming.eat()
print(xiaoming)
print(dir(Person))