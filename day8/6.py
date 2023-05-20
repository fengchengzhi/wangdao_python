class HouseItem:
    def __init__(self, name, area):
        self.name = name
        self.area = area

    def __str__(self):
        return f'家具叫【{self.name}】,占地{str(self.area)}'


class House:
    def __init__(self, name, area):
        self.name = name
        self.free_area = area
        self.total_area = area
        self.item_list = []

    def add_item(self, item: HouseItem):
        if self.free_area < item.area:
            print('面积不够')
        self.free_area -= item.area
        self.item_list += item.name
