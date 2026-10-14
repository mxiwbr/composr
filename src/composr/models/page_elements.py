import uuid
from unittest import case

import regex
from composr.util.i18n import _

class PageElement:
    def __init__(self, label: str):
        self.id = str(uuid.uuid4())
        self.label = label

    def get_type(self) -> str:
        return type(self).__name__

    def get_id(self) -> str:
        return self.id

    def get_label(self) -> str:
        return self.label

class Button(PageElement):
    def __init__(self, label: str, actions = None):
        super().__init__(label)
        self.actions = actions

    def get_actions(self):
        return self.actions

class ListButton(Button):
    def __init__(self, label: str, actions = None):
        super().__init__(label, actions)

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