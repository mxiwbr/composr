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

    def render(self):

        print(self.term.clear + self.term.home, end="")

        self.draw_header("New project")
        self.draw_footer("Controls", "Tab navigate · Enter select · q quit ")

        self.update("options")

    def update(self, region):

        if region == "options":
            with self.term.location(0, 1):
                for i, (key, value) in enumerate(self.options.items()):

                    style = self.term.black_on_silver if self.focused == i else self.term.normal
                    key = self.term.bold + key + self.term.normal

                    # inputs
                    if value != "element.button":
                        option_text = f"\n{key}: {style}{value}{self.term.normal}"
                    # buttons
                    elif value == "element.button":
                        option_text = f"\n[ {style}{key}{self.term.normal} ]"

                    print(f"{self.term.cr + self.term.clear_eol + option_text}")

    def handle_key(self, key):

        match key.name:
            case "KEY_ENTER":
                if self.focused == 3:
                    return {
                        "type": "navigate_page",
                        "parameter": "start_menu",
                    }
            case "KEY_TAB":
                self.focused = (self.focused + 1) % len(self.options)
            case "KEY_BTAB":
                self.focused = (self.focused - 1) % len(self.options)
            case _:
                if str(key) == "\t":
                    self.focused = (self.focused + 1) % len(self.options)
                elif str(key) == "\x1b[Z":
                    self.focused = (self.focused - 1) % len(self.options)

        self.update("options")
        return None
