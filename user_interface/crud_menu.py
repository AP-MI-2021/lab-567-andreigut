
def show_crud_options():
    print('''
    1.Create an inventory item
    2.Read an inventory item by id
    3.Read all items from the inventory
    4.Update an inventory item
    5.Delete an inventory item by id
    x -> Exit CRUD menu.''')


def create_item_option(inventory_services):
    print('Give item information as follows.')
    item_id = input('Item id is=')
    name = input('Name=')
    description = input('Description=')
    acq_price = input('Acquisition price=')
    location = input('Location=')

    try:
        created = inventory_services.create_item(item_id, name, description, acq_price, location)
        return f'Successfully created item {created}'
    except ValueError as err:
        return err.args[0]


def read_item_option(inventory_services):
    item_id = input('Id of the item you want to read is:')
    try:
        found = inventory_services.read_item(item_id)
        return f'For id {item_id}, the item {found} was found.'
    except ValueError as err:
        return err.args[0]


def update_item_option(inventory_services):
    item_id = input('Id of the item you want to update:')
    found = None
    status_components = []
    try:
        found = inventory_services.read_item(item_id)
    except ValueError as err:
        status_components += err.args[0]
    if found is not None:
        print('Give item information as follows.')
        name = input('Name=')
        description = input('Description=')
        acq_price = float(input('Acquisition price='))
        location = input('Location=')
        try:
            update = inventory_services.update_item(item_id, name, description, acq_price, location)
            status_components.append(f'Inventory item {update} was successfully updated with the new values.')
        except ValueError as err1:
            status_components += err1.args[0]
    return status_components


def delete_item_option(services):
    item_id = input('Id of the item you want to update:')
    try:
        deleted = services.delete_item(item_id)
        return f'Item {deleted} was successfully deleted.'
    except ValueError as err:
        return err.args[0]


def run_crud_menu(inventory_services):
    while True:
        show_crud_options()
        option = input('Your option is:')
        if option == '1':
            creation_status = create_item_option(inventory_services)
            print(creation_status)
        elif option == '2':
            read_status = read_item_option(inventory_services)
            print(read_status)
        elif option == '3':
            print(inventory_services.read_all())
        elif option == '4':
            update_status = update_item_option(inventory_services)
            print(update_status)
        elif option == '5':
            delete_status = delete_item_option(inventory_services)
            print(delete_status)
        elif option == 'x':
            break
        else:
            print('Unknown option, try again.')
    print('Exiting CRUD menu.')
