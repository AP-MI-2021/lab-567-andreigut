from logic.crud_proxy import CrudProxy


def show_crud_options():
    print('''
    1.Create an inventory item
    2.Read an inventory item by id
    3.Read all items from the inventory
    4.Update an inventory item
    5.Delete an inventory item by id''')


def create_item_option(crud_proxy):
    print('Give item information as follows.')
    item_id = input('Item id is=')
    name = input('Name=')
    description = input('Description=')
    acq_price = float(input('Acquisition price='))
    location = input('Location=')

    try:
        created = crud_proxy.create_item(item_id, name, description, acq_price, location)
        return f'Successfully created item {created}'
    except ValueError as err:
        return err.args[0]


def read_item_option(crud_proxy):
    item_id = input('Id of the item you want to read is:')
    try:
        found = crud_proxy.read_item(item_id)
        return f'For id {item_id}, the item {found} was found.'
    except ValueError as err:
        return err.args[0]


def update_item_option(crud_proxy):
    item_id = input('Id of the item you want to update:')
    found = None
    status_components = []
    try:
        found = crud_proxy.read_item(item_id)
    except ValueError as err:
        status_components += err.args[0]
    if found is not None:
        print('Give item information as follows.')
        name = input('Name=')
        description = input('Description=')
        acq_price = float(input('Acquisition price='))
        location = input('Location=')
        try:
            update = crud_proxy.update_item(item_id, name, description, acq_price, location)
            status_components.append(f'Inventory item {update} was successfully updated with the new values.')
        except ValueError as err1:
            status_components += err1.args[0]
    return status_components


def delete_item_option(crud_proxy):
    item_id = input('Id of the item you want to update:')
    try:
        deleted = crud_proxy.delete_item(item_id)
        return f'Item {deleted} was successfully deleted.'
    except ValueError as err:
        return err.args[0]


def crud_menu():
    crud_proxy = CrudProxy()
    while True:
        show_crud_options()
        option = input('Your option is:')
        if option == '1':
            creation_status = create_item_option(crud_proxy)
            print(creation_status)
        if option == '2':
            read_status = read_item_option(crud_proxy)
            print(read_status)
        if option == '3':
            print(crud_proxy.read_all())
        if option == '4':
            update_status = update_item_option(crud_proxy)
            print(update_status)
        if option == '5':
            delete_status = delete_item_option(crud_proxy)
            print(delete_status)


crud_menu()
