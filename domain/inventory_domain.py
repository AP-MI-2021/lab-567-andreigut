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


class ItemRegistry:
    def __init__(self):
        self.item_registry = dict({})

    @property
    def item_registry(self):
        return self.__item_registry

    @item_registry.setter
    def item_registry(self, item_registry):
        self.__item_registry = item_registry

    def contains(self, item):
        # checks if item's id is present in registry
        return item.item_id in self.item_registry

    def create(self, item):
        # adds item entry in registry if not already present by id
        if item.item_id not in self.item_registry:
            self.item_registry[item.item_id] = item
            return copy.deepcopy(item)
        else:
            return None

    def read(self, item_id):
        # returns element from registry with id 'item_id', None if there is no entry in registry with that id
        if item_id in self.item_registry:
            return copy.deepcopy(self.item_registry[item_id])
        else:
            return None

    def read_all(self):
        # returns all entries from the registry
        return copy.deepcopy(list(self.item_registry.values()))

    def update(self, item):
        # updates the entry from registry with id 'item_id' if exists, creates it otherwise
        old = None
        if item.item_id in self.item_registry:
            old = copy.deepcopy(self.item_registry[item.item_id])
            self.item_registry[item.item_id] = item
        return old

    def delete(self, item_id):
        # deletes entry with id 'item_id' if exists, returns a copy of the old entry if there was any, None otherwise
        old = None
        if item_id in self.item_registry:
            old = copy.deepcopy(self.item_registry[item_id])
            del self.item_registry[item_id]
        return old
