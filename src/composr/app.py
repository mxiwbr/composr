import sys
from blessed import Terminal
from .pages.start_menu import StartMenu

class App:
    def __init__(self):
        self.term = Terminal()
        self.current_page = "start_menu"

        self.pages = {
            "start_menu": StartMenu(
                self.term,
                self.draw_header,
                self.draw_footer
            )
        }

    def run(self):
        with (
            self.term.fullscreen(),
            self.term.cbreak(),
            self.term.hidden_cursor()
        ):
            self.pages["start_menu"].render()

            while self.current_page != "quit":

                page = self.pages[self.current_page]

                key = self.term.inkey()
                action = page.handle_key(key)
                if action is not None:

                    if action == "quit":
                        sys.exit(0)

                    if action in self.pages:
                        self.current_page = action
                        self.pages[action].render()

    # Draws the header with the application title and version as well as a clock in 24hr format to the top of the screen
    def draw_header(self, title):

        styled_header = self.term.white_on_gray40(
            self.term.center(title)
        )
        print(self.term.home + styled_header, end="", flush=True)

    # Draws a footer with controls overview to the bottom of the screen
    def draw_footer(self):

        with self.term.location(0, self.term.height - 1):
            controls = "↑↓ navigate · Enter select · q quit "
            label = " Controls"

            styled_footer = self.term.white_on_gray40(
                label
                + " " * max(0, self.term.width - len(label) - len(controls))
                + controls
            )
            print(styled_footer, end="", flush=True)
