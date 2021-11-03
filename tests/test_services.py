import unittest
from logic.inventory_services import InventoryManagementServices


class ServicesTestCase(unittest.TestCase):

    def test_undo_redo_throw_exception(self):
        subject = InventoryManagementServices()
        self.assertRaises(ValueError, lambda: subject.redo())
        self.assertRaises(ValueError, lambda: subject.undo())

    def test_undo_redo_after_sequence_of_actions(self):
        subject = InventoryManagementServices()
        item1 = subject.create_item('id', 'name', 'description', '1234.5', 'ABCD')
        item2 = subject.create_item('id1', 'name', 'description', '1234.5', 'ABCD')
        item3 = subject.create_item('id2', 'name', 'description', '1234.5', 'ABCD')
        items = subject.read_all()
        self.assertTrue(len(items) == 3)
        self.assertTrue(item1 in items)
        self.assertTrue(item2 in items)
        self.assertTrue(item3 in items)

        # going downward
        subject.undo()
        items = subject.read_all()
        self.assertTrue(len(items) == 2)
        self.assertTrue(item1 in items)
        self.assertTrue(item2 in items)

        subject.undo()
        items = subject.read_all()
        self.assertTrue(len(items) == 1)
        self.assertTrue(item1 in items)

        subject.undo()
        items = subject.read_all()
        self.assertTrue(len(items) == 0)

        self.assertRaises(ValueError, lambda: subject.undo())

        # going upward
        subject.redo()
        items = subject.read_all()
        self.assertTrue(len(items) == 1)
        self.assertTrue(item1 in items)

        subject.redo()
        items = subject.read_all()
        self.assertTrue(len(items) == 2)
        self.assertTrue(item1 in items)
        self.assertTrue(item2 in items)

        subject.redo()
        items = subject.read_all()
        self.assertTrue(len(items) == 3)
        self.assertTrue(item1 in items)
        self.assertTrue(item2 in items)
        self.assertTrue(item3 in items)

        self.assertRaises(ValueError, lambda: subject.redo())

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
