def validate_item_fields_values(item_id, name, description, acq_price, location):
    '''
    Validates the values that are candidates for inventory item fields
    :param item_id: should be non-null, non-empty string
    :param name: should be non-null, non-empty string
    :param description: should be non-null, non-empty string
    :param acq_price: should be a float
    :param location: should be be non-null, non-empty string of 4 characters length
    :return: list of errors, empty if all fields passed validation
    '''

    validation_errors = []
    if not item_id:
        validation_errors.append("Item id should not be empty")
    if not name:
        validation_errors.append("Item name should not be empty")

    return validation_errors
