import copy
import unittest
from logic.inventory_services import InventoryManagementServices


class ServicesTestCase(unittest.TestCase):

    def test_undo_redo_throw_exception(self):
        subject = InventoryManagementServices()
        self.assertRaises(ValueError, lambda: subject.redo())
        self.assertRaises(ValueError, lambda: subject.undo())

    def test_undo_redo_after_sequence_of_actions(self):
        # 1 inventory is empty
        subject = InventoryManagementServices()

        # 2,3,4 inventory will contain [item1, item2, item3]
        item1 = subject.create_item('id', 'name', 'description', '1234.5', 'ABCD')
        item2 = subject.create_item('id1', 'name', 'description', '1234.5', 'ABCD')
        item3 = subject.create_item('id2', 'name', 'description', '1234.5', 'ABCD')
        items = subject.read_all()
        self.assertTrue(len(items) == 3)
        self.assertTrue(item1 in items)
        self.assertTrue(item2 in items)
        self.assertTrue(item3 in items)

        # going downward with undo 3 times, 4th throws exception
        # 5, removes item3
        subject.undo()
        items = subject.read_all()
        self.assertTrue(len(items) == 2)
        self.assertTrue(item1 in items)
        self.assertTrue(item2 in items)

        # 6, removes item2
        subject.undo()
        items = subject.read_all()
        self.assertTrue(len(items) == 1)
        self.assertTrue(item1 in items)

        # 7, removes item1
        subject.undo()
        items = subject.read_all()
        self.assertTrue(len(items) == 0)

        # 8, nothing to undo, throws exception
        self.assertRaises(ValueError, lambda: subject.undo())

        # 9,  repopulate the registry
        item1 = subject.create_item('id', 'name', 'description', '1234.5', 'ABCD')
        item2 = subject.create_item('id1', 'name', 'description', '1234.5', 'ABCD')
        item3 = subject.create_item('id2', 'name', 'description', '1234.5', 'ABCD')

        # going upward with redo
        # 10, nothing to redo, should throw exception
        self.assertRaises(ValueError, lambda: subject.redo())

        # 11, 2 x undo reverts last 2 additions
        subject.undo()
        subject.undo()
        items = subject.read_all()
        self.assertTrue(item1 in items)
        self.assertTrue(len(items) == 1)

        # 12, reverts last undo
        subject.redo()
        items = subject.read_all()
        self.assertTrue(len(items) == 2)
        self.assertTrue(items == [item1, item2])

        # 13, reverts the first undo
        subject.redo()
        items = subject.read_all()
        self.assertTrue(len(items) == 3)
        self.assertTrue(items == [item1, item2, item3])

        # going back to 1 item
        # 14, 2 x undo reverts last 2 additions
        subject.undo()
        subject.undo()
        items = subject.read_all()
        self.assertTrue(item1 in items)
        self.assertTrue(len(items) == 1)

        # 15, add another item
        item4 = subject.create_item('id4', 'name', 'description', '1234.5', 'ABC1')
        items = subject.read_all()
        self.assertTrue(len(items) == 2)
        self.assertTrue(items == [item1, item4])

        # 16, redo should throw exception
        self.assertRaises(ValueError, lambda: subject.redo())

        # 17, undo should cancel item4 addition
        subject.undo()
        items = subject.read_all()
        self.assertTrue(len(items) == 1)
        self.assertTrue(items == [item1])

        # 18, going back to 14, undo should cancel item1 addition
        subject.undo()
        items = subject.read_all()
        self.assertTrue(len(items) == 0)

        # 19 redo, redo, cancel last 2 undo going back with item1 and item4
        subject.redo()
        subject.redo()
        items = subject.read_all()
        self.assertTrue(len(items) == 2)
        self.assertTrue(items == [item1, item4])

        # 20, redo throws exception
        self.assertRaises(ValueError, lambda: subject.redo())

        # 21 update item
        item_modified = copy.deepcopy(item1)
        item_modified.acq_price = 55.0
        subject.update_item('id', 'name', 'description', 55.0, 'ABCD')
        self.assertTrue(subject.read_all() == [item_modified, item4])

        # 22 undo
        subject.undo()
        self.assertTrue(subject.read_all() == [item1, item4])

    def test_switch_location(self):
        # given registry with 3 items
        subject = InventoryManagementServices()
        item1 = subject.create_item('id', 'name', 'description', '1234.5', 'ABC1')
        item2 = subject.create_item('id1', 'name', 'description', '1234.5', 'ABC2')
        item3 = subject.create_item('id2', 'name', 'description', '1234.5', 'ABC3')

        # should raise error when location strings are not 4 letters
        self.assertRaises(ValueError, lambda: subject.switch_location('notOString', 'okst'))

        # should raise error when initial location is not found
        self.assertRaises(ValueError, lambda: subject.switch_location('UKNW', 'ABCD'))

        # should change location when parameters are ok and location already exists
        from_location = 'ABC2'
        to_location = 'ABCD'
        subject.switch_location(from_location, to_location)
        items = subject.read_all()
        self.assertTrue(len(items) == 3)
        self.assertTrue(item1 in items)
        self.assertTrue(item3 in items)
        self.assertTrue(subject.read_item(item2.item_id).location == to_location)

    def test_append_description_for_items_with_price_bigger_than(self):
        # given registry with 3 items
        subject = InventoryManagementServices()
        item1 = subject.create_item('id', 'name', 'description', '1234.5', 'ABC1')
        item2 = subject.create_item('id1', 'name', 'description', '78', 'ABC2')
        item3 = subject.create_item('id2', 'name', 'description', '23', 'ABC3')

        # should raise error when input is not correct:
        # raise error for price
        self.assertRaises(ValueError, lambda: subject.append_description_for_items_with_price_bigger_than('123d', 'DE'))
        # raise error for description
        self.assertRaises(ValueError, lambda: subject.append_description_for_items_with_price_bigger_than('123', ''))

        # should raise error when no item has price bigger than given price:
        self.assertRaises(ValueError, lambda: subject.append_description_for_items_with_price_bigger_than('2000', 'DE'))

        # should append description for items with price bigger than given price:
        subject.append_description_for_items_with_price_bigger_than('50', 'append')
        expected_description = 'descriptionappend'
        old_description = 'description'
        self.assertTrue(subject.read_item(item1.item_id).description == expected_description)
        self.assertTrue(subject.read_item(item2.item_id).description == expected_description)
        self.assertTrue(subject.read_item(item3.item_id).description == old_description)

    def test_get_max_price_by_location_and_get_total_price_by(self):
        # given registry with 5 items
        subject = InventoryManagementServices()
        subject.create_item('id', 'name', 'description', '1234.5', 'ABC1')
        subject.create_item('id1', 'name', 'description', '78', 'ABC2')
        subject.create_item('id7', 'name', 'description', '80', 'ABC2')
        subject.create_item('id2', 'name', 'description', '23', 'ABC4')
        subject.create_item('id4', 'name', 'description', '2000', 'ABC1')

        # then should compute max price per location and total price per location
        self.assertTrue(
            subject.get_biggest_price_by_location() == {'ABC1': float(2000), 'ABC2': float(80), 'ABC4': float(23)})
        self.assertTrue(
            subject.get_total_price_by_location() == {'ABC1': 3234.5, 'ABC2': float(158), 'ABC4': float(23)})

    def test_sort_ascending_by_price(self):
        # given registry with 3 items
        subject = InventoryManagementServices()
        item1 = subject.create_item('id', 'name', 'description', '1234.5', 'ABC1')
        item2 = subject.create_item('id1', 'name', 'description', '78', 'ABC2')
        item3 = subject.create_item('id2', 'name', 'description', '23', 'ABC3')

        # should sort them by ascending price
        subject.sort_by_acq_price_ascending()
        actual = subject.read_all()
        self.assertTrue(actual == [item3, item2, item1])
