from logic.inventory_services import InventoryManagementServices
from user_interface.crud_menu import run_crud_menu


def show_main_options():
    print('''
    1.Access crud menu
    2.Move items from a location to another
    3.Append description for items with price bigger than a given price.
    4.Undo from current state.
    5.Redo from current state.
    6.Show registry current state
    x -> Exit main menu.''')


def switch_locations_option(services):
    print('Move items from a location to another.')
    from_location = input('Give current location you want to change=')
    to_location = input('Give destination location=')
    try:
        services.switch_location(from_location, to_location)
        return 'Location was switched successfully.'
    except ValueError as err:
        return err.args[0]


def add_description_for_bigger_price_than_given_price_option(services):
    print('Add description for items with price bigger than given price.')
    given_price = input('Given price=')
    description = input('Description to append=')
    try:
        services.append_description_for_items_with_price_bigger_than(given_price, description)
        return 'Description was added successfully.'
    except ValueError as err:
        return err.args[0]


def main_menu():
    services = InventoryManagementServices()
    while True:
        show_main_options()
        option = input('Your option is:')
        if option == '1':
            run_crud_menu(services)
        elif option == '2':
            print(switch_locations_option(services))
        elif option == '3':
            print(add_description_for_bigger_price_than_given_price_option(services))
        elif option == '4':
            services.undo()
        elif option == '5':
            services.redo()
        elif option == '6':
            print(services.read_all())
        elif option == 'x':
            break
        else:
            print('Unknown option, try again.')
    print('Exiting main menu.')


main_menu()
