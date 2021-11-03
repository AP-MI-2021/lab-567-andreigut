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
        validation_errors.append("Item id should not be empty.")
    if not name:
        validation_errors.append("Item name should not be empty.")
    if not description:
        validation_errors.append("Item description should not be empty.")
    if len(location) != 4:
        validation_errors.append("Location should be a 4 letter string.")
    if not validate_price_is_float(acq_price):
        validation_errors.append("Acquisition price should be a string convertible to float.")

    return validation_errors


def validate_price_is_float(price):
    '''
    Validates if price is a string that can be converted to float.
    :param price: representation of price as string, provided by user
    :return: True if price represents a float, False otherwise.
    '''
    try:
        float(price)
        return True
    except ValueError:
        return False
