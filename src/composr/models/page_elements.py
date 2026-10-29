import uuid
from enum import Enum

import regex

from composr.models.service import Service
from composr.util.i18n import _

class PageElement:

    def __init__(self, label: str, selectable: bool = True):
        self.id = str(uuid.uuid4())
        self.label = label
        self.__selectable = selectable

    def get_type(self) -> str:
        return type(self).__name__

    def get_id(self) -> str:
        return self.id

    def get_label(self) -> str:
        return self.label

    def is_selectable(self) -> bool:
        return self.__selectable

class Button(PageElement):
    def __init__(self, label: str, actions = None):
        super().__init__(label)
        self.actions = actions

    def get_actions(self):
        return self.actions

class ListButton(Button):
    def __init__(self, label: str, actions = None):
        super().__init__(label, actions)

class CycleButton(PageElement):

    # tuple[value, display]
    def __init__(self, label: str, items: list[tuple[str, str]] | list[tuple[int, Service]] | None = None, default_selected_value: str | int | None = None):
        super().__init__(label)

        self.selected = 0

        self.items = items or []

        if items is not None and default_selected_value is not None:
            self.select_item(default_selected_value)

        self.changed = False

    def get_items(self):
        return self.items

    def get_selected(self):
        return self.items[self.selected]

    def move_selection(self, direction: int):
        self.selected = (self.selected + direction) % len(self.items)

    def select_item(self, value):
        for i, item in enumerate(self.items):
            if item[0] == value:
                self.selected = i

class NavigatorList(CycleButton):
    def __init__(
            self,
            label: str,
            empty_message: str = _("No items added yet."),
            items: list[tuple[str, str]] | list[tuple[int, Service]] | None = None,
            default_selected_value: str | int | None = None
    ):
        super().__init__(label, items, default_selected_value)
        self.empty_message = empty_message

    def is_empty(self) -> bool:
        return len(self.items) == 0

    def is_selectable(self) -> bool:
        return len(self.items) > 0

    # Returns False if the end or the beginning (depending on the direction) is already selected to be able to switch to the next page item
    def move_selection(self, direction: int) -> bool:

        new_index = self.selected + direction

        if not 0 <= new_index < len(self.items):
            return False

        self.selected = new_index
        return True

    def get_actions(self) -> list[dict[str, str]] | None:
        actions: list[dict[str, str]] = [
            {
                "type": "suspend_previous_page_save",
                "parameter": ""
            }
        ]

        if len(self.items) > 0 and isinstance(self.items[0][1], Service):
            for item in self.items:
                actions.append({
                    "type": "navigate_page",
                    "parameter": "service_editor",
                    "page_parameter": item[0],
                })
            return actions
        else:
            return None


class InputField(PageElement):
    def __init__(self,
                 label: str,
                 value: str = "",
                 input_char_pattern: str = r"^(?:\p{L}|\d)$",
                 validation_pattern: str = r"^(?:\p{L}|\d)+$",
                 validation_message: str = _("Input may only contain letters and numbers! ")
    ):
        super().__init__(label)

        self.value = value
        self.input_char_pattern = input_char_pattern
        self.validation_pattern = validation_pattern
        self.validation_message = validation_message

    def get_value(self) -> str:
        return self.value

    def set_value(self, value: str):
        self.value = value

    def validate_input(self, text: str):

        pattern = regex.compile(self.input_char_pattern, regex.VERSION1)

        if pattern.match(text):
            return True
        else:
            return False

    def validate_value(self):

        pattern = regex.compile(self.validation_pattern, regex.VERSION1)

        if pattern.match(self.value):
            return True
        else:
            return self.validation_message

class Placeholder(PageElement):
    class PlaceholderType(Enum):
        TAB = "\t"
        LINE = "\n"
        WHITESPACE = " "

    def __init__(self, ph_type: PlaceholderType):
        super().__init__(ph_type.value, False)