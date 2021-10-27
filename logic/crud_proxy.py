from domain.inventory_domain import ItemRegistry
from domain.inventory_domain import InventoryItem
from logic.validation import validate_item_fields_values


class CrudProxy:
    def __init__(self):
        self.__registry = ItemRegistry()

    def create_item(self, item_id, name, description, acq_price, location):
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
            found = self.__registry.delete(item_id)
        if found is not None:
            return found
        else:
            errors.append(f'No entry with item id={item_id} present in registry.')
        if not errors:
            return found
        else:
            raise ValueError(errors)
