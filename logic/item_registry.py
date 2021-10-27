import copy


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
