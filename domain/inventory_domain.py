import copy


class InventoryItem:
    def __init__(self, item_id, name, description, acq_price, location):
        self.item_id = item_id
        self.name = name
        self.description = description
        self.acq_price = acq_price
        self.location = location

    def __str__(self):
        return "InventoryItem([{0},{1},{2},{3},{4}])".format(self.item_id, self.name, self.description, self.acq_price,
                                                             self.location)

    def __repr__(self):
        return "InventoryItem([{0},{1},{2},{3},{4}])".format(self.item_id, self.name, self.description, self.acq_price,
                                                             self.location)

    def __eq__(self, other):
        if not isinstance(other, InventoryItem):
            return False
        return self.item_id == other.item_id and self.name == other.name and self.description == other.description and \
               self.acq_price == other.acq_price and self.location == other.location

    @property
    def item_id(self):
        return self.__item_id

    @item_id.setter
    def item_id(self, item_id):
        self.__item_id = item_id

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, description):
        self.__description = description

    @property
    def acq_price(self):
        return self.__acq_price

    @acq_price.setter
    def acq_price(self, acq_price):
        self.__acq_price = acq_price

    @property
    def location(self):
        return self.__location

    @location.setter
    def location(self, location):
        self.__location = location



