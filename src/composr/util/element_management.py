def get_element_by_id(elements: list, element_id: str):
    for element in elements:
        if element.get_id() == element_id:
            return element
    return None