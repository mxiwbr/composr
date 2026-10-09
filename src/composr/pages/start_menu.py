import importlib.metadata
from blessed import Terminal

app_version = importlib.metadata.version("composr")

class StartMenu:
    def __init__(self, term: Terminal, draw_header, draw_footer):

        self.term = term
        self.draw_header = draw_header
        self.draw_footer = draw_footer

        self.selected = 0
        self.options = [
            "Create new compose file",
            "Quit"
        ]

    def render(self):

        print(self.term.clear + self.term.home, end="")

        self.draw_header(f"Composr v{app_version}")
        self.draw_footer()

        print(
            self.term.move_y(1)
            + "\nWelcome to Composr!\n"
            + self.term.darkgray
            + "A terminal application for building docker compose files\n"
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
                self.selected = max(0, self.selected - 1)
            case "KEY_DOWN":
                self.selected = min(max(0, len(self.options) - 1), self.selected + 1)
            case "KEY_ENTER":
                if self.selected == 1:
                    return "quit"
            case _:
                if str(key) == "\n" or str(key) == "q":
                    return "quit"

        self.update("options")
        return None