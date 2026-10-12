import uuid
import regex

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
    def __init__(self, label: str, action_type = None, action_param = None):
        super().__init__(label)
        self.action = {
            "type": action_type,
            "parameter": action_param
        }

    def get_action(self) -> dict:
        return self.action

class InputField(PageElement):
    def __init__(self, label: str, value: str = "", allowed_chars: str = r"^\p{L}+$"):
        super().__init__(label)
        self.value = value
        self.allowed_chars = allowed_chars

    def get_value(self) -> str:
        return self.value

    def set_value(self, value: str):
        self.value = value

    def validate_input(self, text: str):
        pattern = regex.compile(self.allowed_chars, regex.VERSION1)

        if pattern.match(text):
            return True
        else:
            return False