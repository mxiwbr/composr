from blessed import Terminal

from composr.models.page_elements import InputField, Button

class CreateProject:
    def __init__(self, term: Terminal, draw_header, draw_footer):

        self.term = term
        self.draw_header = draw_header
        self.draw_footer = draw_footer

        self.elements = [
            InputField("Project name", "my-compose", "^[\p{L}\-_]+$"),
            InputField("Filename", "docker-compose.yml", "^[\p{L}\-_.]+$"),
            Button("Continue"),
            Button("Cancel", "navigate_page", "start_menu"),
        ]

        self.focused = self.elements[0].get_id()

        self.edit = None
        self.input_buffer = ""

    def render(self):

        print(self.term.clear + self.term.home, end="")

        self.draw_header("New project")

        self.update("elements")
        self.update("footer")

    def update(self, region):

        if region == "elements":

            last_element = None

            with self.term.location(0, 2):
                for element in self.elements:

                    style = self.term.black_on_silver if self.focused == element.get_id() else self.term.normal

                    # Input (Edit) mode
                    if self.edit is not None and element.get_type() != "Button" and self.edit == element.get_id():

                        self.focused = None
                        style = self.term.normal

                        label = self.term.bold + element.get_label() + self.term.normal
                        option_text = f"{label}: {style}{element.get_value()}{self.term.normal}|"

                        print(f"{self.term.cr + self.term.clear_eol + option_text}")

                        last_element = element.get_type()

                    # inputs
                    elif element.get_type() != "Button":

                        label = self.term.bold + element.get_label() + self.term.normal
                        option_text = f"{label}: {style}{element.get_value()}{self.term.normal}"

                        print(f"{self.term.cr + self.term.clear_eol + option_text}")

                        last_element = element.get_value()

                    # buttons
                    elif element.get_type() == "Button":

                        label = (self.term.bold + element.get_label() + self.term.normal) if self.focused != element.get_id() else element.get_label()
                        option_text = f"[ {style}{label}{self.term.normal} ]"

                        if last_element == "Button":
                            print(f"\t{option_text}", end="")
                        else:
                            print(f"\n{self.term.cr + self.term.clear_eol + option_text}", end="")

                        last_element = element.get_type()

        elif region == "footer":
            if self.edit is None:
                self.draw_footer(" Controls", "↑↓ navigate · Enter select · Q quit ")
            else:
                self.draw_footer(" Controls", "Enter Confirm changes")

    def handle_key(self, key):

        if self.edit is None:

            element = next(element for element in self.elements if element.get_id() == self.focused)

            match key.name:
                case "KEY_ENTER":
                    if element.get_type() != "Button":
                        self.edit = element.get_id()
                        self.update("footer")
                    elif element.get_type() == "Button":
                        return element.get_action()
                case "KEY_DOWN":
                    elements = iter(self.elements)
                    next(element for element in elements if element.get_id() == self.focused)
                    self.focused = next(elements, self.elements[0]).get_id()
                case "KEY_UP":
                    elements = reversed(self.elements)
                    next(element for element in elements if element.get_id() == self.focused)
                    self.focused = next(elements, self.elements[-1]).get_id()
                case _:
                    if str(key) == "\n":
                        if element.get_type() == "Button":
                            return element.get_action()
        else:

            element = next(element for element in self.elements if element.get_id() == self.edit)

            match key.name:
                case "KEY_ENTER":
                    self.focused = self.edit
                    self.edit = None
                    self.update("footer")
                case "KEY_BACKSPACE":
                    element.set_value(element.get_value()[:-1])
                case _:
                    if str(key) == "\n":
                        self.focused = self.edit
                        self.edit = None
                        self.update("footer")
                    else:
                        char = str(key)
                        if len(char) == 1 and (element.validate_input(char)):
                            element.set_value(element.get_value() + str(key))
        self.update("elements")
        return None
