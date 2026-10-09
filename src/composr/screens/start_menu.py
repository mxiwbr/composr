from blessed import Terminal

class StartMenu:
    def __init__(self, term: Terminal, draw_header, draw_footer):

        self.term = term
        self.draw_header = draw_header
        self.draw_footer = draw_footer

        self.selected = 0
        self.options = [
            "New Project",
            "Quit"
        ]

    def render(self):

        print(self.term.clear + self.term.home, end="")

        self.draw_header()
        self.draw_footer(" Controls", "↑↓ navigate · Enter select · Q quit ")

        print(
            self.term.move_y(1)
            + self.term.bold
            + "\nWelcome to Composr!\n"
            + self.term.normal
            + self.term.darkgray
            + "A terminal application for building docker compose files\n"[:self.term.width - 1]
            + self.term.normal
        )

        self.update("options")

    def update(self, region):
        if region == "options":
            print(self.term.move_y(4))
            for i, option in enumerate(self.options):
                print(f"{self.term.cr + self.term.clear_eol + self.term.bold}{">" if self.selected == i else self.term.normal} {option + self.term.normal}")

    def handle_key(self, key):

        match key.name:
            case "KEY_UP":
                self.selected = (self.selected - 1) % len(self.options)
            case "KEY_DOWN":
                self.selected = (self.selected + 1) % len(self.options)
            case "KEY_ENTER":
                if self.selected == 1:
                    return { "type": "quit" }
                elif self.selected == 0:
                    return {
                        "type": "navigate_page",
                        "parameter": "create_project"
                    }
            case _:
                if str(key) == "\n" or str(key) == "q":
                    return { "type": "quit" }

        self.update("options")
        return None