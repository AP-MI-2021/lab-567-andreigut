
from domain.inventory_domain import InventoryItem


def test_inventory_item_constructor_and_getters():
    subject = InventoryItem('id', 'name', 'description', 123, 'abcd')
    assert subject.item_id == 'id'
    assert subject.name == 'name'
    assert subject.description == 'description'
    assert subject.acq_price == 123
    assert subject.location == 'abcd'


def test_inventor_item_setters():
    subject = InventoryItem('id', 'name', 'description', 123, 'abcd')
    subject.item_id = 'new id'
    subject.name = 'new name'
    subject.description = 'new description'
    subject.acq_price = 124
    subject.location = 'wxyz'
    assert subject.item_id == 'new id'
    assert subject.name == 'new name'
    assert subject.description == 'new description'
    assert subject.acq_price == 124
    assert subject.location == 'wxyz'


def test_all_domain():
    test_inventory_item_constructor_and_getters()
    test_inventor_item_setters()
