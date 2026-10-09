from blessed import Terminal

class CreateProject:
    def __init__(self, term: Terminal, draw_header, draw_footer):

        self.term = term
        self.draw_header = draw_header
        self.draw_footer = draw_footer

        self.focused = 0
        self.options = {
            "Project name": "my-compose",
            "Filename": "docker-compose.yml",
            "Continue": "element.button",
            "Cancel": "element.button",
        }

        self.edit = None
        self.input_buffer = ""

    def render(self):

        print(self.term.clear + self.term.home, end="")

        self.draw_header("New project")

        self.update("options")
        self.update("footer")

    def update(self, region):

        if region == "options":

            last_element = None

            with self.term.location(0, 2):
                for i, (key, value) in enumerate(self.options.items()):

                    style = self.term.black_on_silver if self.focused == i else self.term.normal

                    # Input (Edit) mode
                    if self.edit is not None and value != "element.button" and self.edit == i:

                        self.focused = None
                        style = self.term.normal

                        key = self.term.bold + key + self.term.normal
                        option_text = f"{key}: {style}{value}{self.term.normal}|"

                        print(f"{self.term.cr + self.term.clear_eol + option_text}")

                        last_element = value

                    # inputs
                    elif value != "element.button":

                        key = self.term.bold + key + self.term.normal
                        option_text = f"{key}: {style}{value}{self.term.normal}"

                        print(f"{self.term.cr + self.term.clear_eol + option_text}")

                        last_element = value

                    # buttons
                    elif value == "element.button":

                        key = (self.term.bold + key + self.term.normal) if self.focused != i else key
                        option_text = f"[ {style}{key}{self.term.normal} ]"

                        if last_element == "element.button":
                            print(f"\t{option_text}", end="")
                        else:
                            print(f"\n{self.term.cr + self.term.clear_eol + option_text}", end="")

                        last_element = value

        elif region == "footer":
            if self.edit is None:
                self.draw_footer(" Controls", "↑↓ navigate · Enter select · Q quit ")
            else:
                self.draw_footer(" Controls", "Enter Confirm changes")

    def handle_key(self, key):

        if self.edit is None:
            match key.name:
                case "KEY_ENTER":
                    if self.focused < 2:
                        self.edit = self.focused
                        self.update("footer")
                    elif self.focused == 3:
                        return {
                            "type": "navigate_page",
                            "parameter": "start_menu",
                        }
                case "KEY_DOWN":
                    self.focused = (self.focused + 1) % len(self.options)
                case "KEY_UP":
                    self.focused = (self.focused - 1) % len(self.options)
                case _:
                    if str(key) == "\n":
                        if self.focused == 3:
                            return {
                                "type": "navigate_page",
                                "parameter": "start_menu",
                            }
        else:
            match key.name:
                case "KEY_ENTER":
                    self.focused = self.edit
                    self.edit = None
                    self.update("footer")
                case "KEY_BACKSPACE":
                    self.options.update({list(self.options)[self.edit]: list(self.options.values())[self.edit][:-1]})
                case _:
                    if str(key) == "\n":
                        self.focused = self.edit
                        self.edit = None
                        self.update("footer")
                    else:
                        char = str(key)
                        if len(char) == 1 and (char.isalpha() or char in ['-', '_']):
                            self.options.update({list(self.options)[self.edit]: list(self.options.values())[self.edit] + str(key)})
        self.update("options")
        return None
