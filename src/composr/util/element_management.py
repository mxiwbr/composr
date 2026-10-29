def get_element_by_id(elements: list, element_id: str):
    for element in elements:
        if element.get_id() == element_id:
            return element
    return None

def get_first_selectable_element_id(elements: list):
    return next((element.get_id() for element in elements if element.is_selectable()), None)