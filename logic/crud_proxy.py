from logic.item_registry import ItemRegistry
from domain.inventory_domain import InventoryItem
from logic.validation import validate_item_fields_values


class CrudProxy:
    '''
    A proxy for basic crud operations with IventoryItems against an IventoryRegistry.
    '''
    def __init__(self):
        self.__registry = ItemRegistry()

    def create_item(self, item_id, name, description, acq_price, location):
        '''Creates an InventoryItem from given params and persists it.

                Args:
                    item_id (string): item id
                    name (string): item name
                    description (string)
                    acq_price (float): The acquisition price for item.

                Raises: ValueError: item_id, name, description are nullable, location is not 4 letters string or
                acq_price is not a float.

                Returns:
                    created: A copy for the item that was created.


        '''
        errors = validate_item_fields_values(item_id, name, description, acq_price, location)
        created = None
        if not errors:
            conv_price = float(acq_price)
            created = self.__registry.create(InventoryItem(item_id, name, description, conv_price, location))
            if created is None:
                errors.append('Already exists and item in the registry with id')
        if not errors:
            return created
        else:
            raise ValueError(errors)

    def read_item(self, item_id):
        ''' Reads an item from the registry using the given id.

                        Args:
                            item_id (string): Id, name, description and location for the given item.
                            acq_price (float): The acquisition price for item.

                        Raises: ValueError: item_id, name, description are nullable, location is not 4 letters string or
                        acq_price is not a float.

                        Returns:
                            created: A copy for the item that was created.
        '''
        errors = []
        found = None
        if not item_id:
            errors.append('Item id should be a non-null and non-empty string.')
        else:
            found = self.__registry.read(item_id)
        if found is None and not errors:
            errors.append(f'No entry with id={item_id} has been found in the registry')
        if not errors:
            return found
        else:
            raise ValueError(errors)

    def read_all(self):
        return self.__registry.read_all()

    def update_item(self, item_id, name, description, acq_price, location):
        errors = validate_item_fields_values(item_id, name, description, acq_price, location)
        if not errors:
            conv_price = float(acq_price)
            return self.__registry.update(InventoryItem(item_id, name, description, conv_price, location))
        else:
            raise ValueError(errors)

    def delete_item(self, item_id):
        errors = []
        found = None
        if not item_id:
            errors.append('Item id should be a non-null and non-empty string.')
        if not errors:
            found = self.__registry.delete(item_id)
        if found is not None:
            return found
        else:
            errors.append(f'No entry with item id={item_id} present in registry.')
        if not errors:
            return found
        else:
            raise ValueError(errors)

    def override_registry(self, items):
        self.__registry.override_state(items)