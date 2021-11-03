import copy

from logic.crud_proxy import CrudProxy
from domain.inventory_domain import InventoryItem
from logic.validation import validate_price_is_float


class InventoryManagementServices:
    '''
    A gateway to all the services required by the UI.
    '''

    def __init__(self):
        self.__delegate_crud_proxy = CrudProxy()
        self.__current = []
        self.__undo = []
        self.__redo = []

    def state_snapshot(self):
        self.__undo.append(self.__current)
        self.__current = self.__delegate_crud_proxy.read_all()
        self.__redo.clear()

    def create_item(self, item_id, name, description, acq_price, location):
        created = self.__delegate_crud_proxy.create_item(item_id, name, description, acq_price, location)
        self.state_snapshot()
        return created

    def read_item(self, item_id):
        return self.__delegate_crud_proxy.read_item(item_id)

    def read_all(self):
        return self.__delegate_crud_proxy.read_all()

    def update_item(self, item_id, name, description, acq_price, location):
        updated = self.__delegate_crud_proxy.update_item(item_id, name, description, acq_price, location)
        self.state_snapshot()
        return updated

    def delete_item(self, item_id):
        deleted = self.__delegate_crud_proxy.delete_item(item_id)
        self.state_snapshot()
        return deleted

    def switch_location(self, from_location, to_location):
        '''
        Switch location for all items that have current location 'from_location', with 'to_location'.
        Throws ValueError if input is not location pattern or there are no items with given 'from_location'.
        :param from_location: current location
        :param to_location: future location
        :return: Nothing.
        '''
        if len(from_location) != 4 or len(to_location) != 4:
            raise ValueError('Locations should be 4 letters strings.')
        items = self.read_all()
        elements_at_old_location = any(item.location == from_location for item in items)
        if not elements_at_old_location:
            raise ValueError(f'There are no elements with location {from_location}')
        new_items = []
        for item in items:
            if item.location == from_location:
                new_items.append(InventoryItem(item.item_id, item.name, item.description, item.acq_price, to_location))
            else:
                new_items.append(item)
        self.__delegate_crud_proxy.override_registry(new_items)

    def append_description_for_items_with_price_bigger_than(self, given_price, description):
        '''
        Appends given 'description' to current description for all items having the acquisition price bigger than
        'given_price'.
        :param given_price: Given price to check against.
        :param description: Description to be appended.
        :return: Nothing
        '''
        if not validate_price_is_float(given_price):
            raise ValueError('Given price should be a string representation of a float.')
        if not description:
            raise ValueError('Description should be a non empty string.')
        price = float(given_price)
        items = self.read_all()
        new_items = []
        found = False
        for item in items:
            if item.acq_price > price:
                found = True
                new_items.append(InventoryItem(item.item_id, item.name, item.description + description, item.acq_price, item.location))
            else:
                new_items.append(item)
        if found:
            self.__delegate_crud_proxy.override_registry(new_items)
        else:
            raise ValueError(f"No item with price bigger than {price} has been found.")

    def undo(self):
        """
        Should undo registry state to previous of last modification.
        Throws ValueError exception if there is no state to go back.
        :return: nothing
        """
        if not self.__undo:
            raise ValueError("No previous state to go back.")
        self.__redo.append(self.__current)
        self.__current = copy.deepcopy(self.__undo.pop())
        self.__delegate_crud_proxy.override_registry(self.__current)

    def redo(self):
        """
        Should redo as reverse action of undo.
        Throws ValueError exception if there is no undo to be reversed.
        :return: nothing
        """
        if not self.__redo:
            raise ValueError("No previous undo to be reversed.")
        self.__undo.append(self.__current)
        self.__current = copy.deepcopy(self.__redo.pop())
        self.__delegate_crud_proxy.override_registry(self.__current)
