from logic.inventory_services import InventoryManagementServices
from user_interface.crud_menu import run_crud_menu
import tests.test_domain
import tests.test_logic


def show_main_options():
    print('''
    1.Access crud menu
    2.Move items from a location to another
    3.Append description for items with price bigger than a given price.
    4.Get biggest price per location.
    5.Order ascending by acq price.
    6.Get total price per location.
    7.Undo from current state.
    8.Redo from current state.
    9.Show registry current state
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


def order_by_price_option(services):
    services.sort_by_acq_price_ascending()
    return f'Item in ascending order by acq price are: {services.read_all()}'


def undo_option(services):
    try:
        services.undo()
        return 'Undo was done successfully.'
    except ValueError as err:
        return err.args[0]


def redo_option(services):
    try:
        services.redo()
        return 'Redo was done successfully.'
    except ValueError as err:
        return err.args[0]


def main_menu():
    services = InventoryManagementServices()
    # before
    services.create_item('id1', 'name1', 'descr1', '25', 'abcd')
    services.create_item('id3', 'name3', 'descr3', '30', 'abcd')
    services.create_item('id2', 'name2', 'descr2', '17', 'dfgh')

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
            print(f'Biggest price by location: {services.get_biggest_price_by_location()}')
        elif option == '5':
            print(order_by_price_option(services))
        elif option == '6':
            print(f'Total price by location: {services.get_total_price_by_location()}')
        elif option == '7':
            print(undo_option(services))
        elif option == '8':
            print(redo_option(services))
        elif option == '9':
            print(services.read_all())
        elif option == 'x':
            break
        else:
            print('Unknown option, try again.')
    print('Exiting main menu.')


tests.test_domain.test_all_domain()
tests.test_logic.test_all_logic()

main_menu()


# def help_menu():
#     print("""1. To add an item you must provide the following command: add,<item_id>,<name>,<description>,<acq_price>,<location>
#        2. To show all items from the inventory you must provide the following command: showall
#        3. To delete an item from the inventory you must provide the following command: delete,<item_id>
#        4. You can also use aggregated commands that would look like this:
#          add,1,nume,descriere,32,abcd;showall;delete,3
#        as a single line string.
#         A simple command would look like this: delete,3
#         As you can notice commands are separated by ';'
#        'x' command will close the console menu
#     """)
#
#
# def handle_add_command(services, command):
#     args = command.split(',')
#     if len(args) != 6:
#         return 'Not enough args for add command'
#     try:
#         created = services.create_item(args[1], args[2], args[3], args[4], args[5])
#         return f'Item {created} was successfully created.'
#     except ValueError as err:
#         return err.args[0]
#
#
# def handle_delete_command(services, command):
#     args = command.split(',')
#     if len(args) != 2:
#         return 'Not enough args for this delete command'
#     try:
#         deleted = services.delete_item(args[1])
#         return f'Item {deleted} was successfully deleted.'
#     except ValueError as err:
#         return err.args[0]
#
#
# def command_line_console():
#     services = InventoryManagementServices()
#     while True:
#         help_menu()
#         agg_command = input("your command is=")
#         commands = agg_command.split(';')
#         for command in commands:
#             if command == 'showall':
#                 print(services.read_all())
#             elif command.startswith('add'):
#                 print(handle_add_command(services, command))
#             elif command.startswith('delete'):
#                 print(handle_delete_command(services, command))
#             elif command == 'x':
#                 break
#             else:
#                 print('Unknown command, try again.')
#         if 'x' in commands:
#             break
#     print('Closing console menu')
#
# # add,id1,name1,descr1,123,abcd; add,id1,name1,descr1,123,abcd;add,id2,name1,descr1,123,abcd;showall;add,id3,name1,descr1,123,abcd;delete,id1;showall
