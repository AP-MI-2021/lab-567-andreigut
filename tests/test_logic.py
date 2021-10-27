from domain.inventory_domain import InventoryItem
from logic.item_registry import ItemRegistry
import copy


def test_item_registry_constructor_and_getters_setters():
    subject = ItemRegistry()
    assert subject.item_registry == {}
    item = InventoryItem('id', 'name', 'description', 123, 'abcd')
    dictionary = {item.item_id: item}
    subject.item_registry = dictionary
    assert subject.item_registry == dictionary


def test_item_registry_create():
    # given registry and 2 items to be created
    subject = ItemRegistry()
    first_item = InventoryItem('id1', 'name1', 'description1', 123, 'abc1')
    second_item = InventoryItem('id2', 'name2', 'description2', 124, 'abc2')

    # when create should store in item_registry
    subject.create(first_item)
    subject.create(second_item)
    assert len(subject.item_registry.keys()) == 2
    registry_values = list(subject.item_registry.values())
    assert first_item in registry_values
    assert second_item in registry_values

    # when create an already exiting item do not modify registry
    registry_snapshot = dict(subject.item_registry)
    first_item_clone = copy.deepcopy(first_item)
    subject.create(first_item_clone)
    assert subject.item_registry == registry_snapshot


def test_item_registry_read_and_read_all():
    # given registry with 2 items
    subject = ItemRegistry()
    first_item = InventoryItem('id1', 'name1', 'description1', 123, 'abc1')
    second_item = InventoryItem('id2', 'name2', 'description2', 124, 'abc2')
    subject.create(first_item)
    subject.create(second_item)

    # when read should return by id
    assert subject.read(first_item.item_id) == first_item
    assert subject.read(second_item.item_id) == second_item
    assert subject.read('unknown id') is None

    # when read all should return registry values
    registry_values = subject.read_all()
    assert len(registry_values) == 2
    assert first_item in registry_values
    assert second_item in registry_values


def test_item_registry_update():
    # given registry with 1 item and 1 un-associated item
    subject = ItemRegistry()
    first_item = InventoryItem('id1', 'name1', 'description1', 123, 'abc1')
    second_item = InventoryItem('id2', 'name2', 'description2', 124, 'abc2')
    subject.create(first_item)

    # when update existing item should replace
    first_item_copy = copy.deepcopy(first_item)
    first_item_copy.name = "new name"
    subject.update(first_item_copy)
    assert subject.read(first_item.item_id).name == "new name"

    # when update non-existing item should ignore
    subject.update(second_item)
    assert subject.read(second_item.item_id) is None


def test_item_registry_delete():
    # given registry with 1 item
    subject = ItemRegistry()
    first_item = InventoryItem('id1', 'name1', 'description1', 123, 'abc1')
    subject.create(first_item)

    # when delete non-existing id should do nothing
    registry_snapshot = dict(subject.item_registry)
    subject.delete('unknown id')
    assert subject.item_registry == registry_snapshot

    # should delete existing id
    assert subject.read(first_item.item_id) == first_item
    subject.delete(first_item.item_id)
    assert subject.read(first_item.item_id) is None


def test_all_logic():
    test_item_registry_constructor_and_getters_setters()
    test_item_registry_create()
    test_item_registry_read_and_read_all()
    test_item_registry_update()
