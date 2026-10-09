import importlib.metadata
import sys

from blessed import Terminal

from .screens.create_project import CreateProject
from .screens.start_menu import StartMenu

app_version = importlib.metadata.version("composr")

class App:
    def __init__(self):
        self.term = Terminal()
        self.current_page = "start_menu"
        self.compose_project = None

        self.pages = {
            "start_menu": StartMenu(
                self.term,
                self.draw_header,
                self.draw_footer
            ),
            "create_project": CreateProject(
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

            last_termsize = (self.term.width, self.term.height)
            self.pages["start_menu"].render()

            while self.current_page != "quit":

                page = self.pages[self.current_page]

                key = self.term.inkey(timeout=0.25)
                current_termsize = (self.term.width, self.term.height)

                if current_termsize != last_termsize:
                    last_termsize = current_termsize
                    page.render()

                if not key:
                    continue

                action = page.handle_key(key)

                if action is not None:

                    action_type = action.get("type")
                    action_param = action.get("parameter")

                    if action_type == "quit":
                        sys.exit(0)

                    if action_type == "navigate_page" and action_param in self.pages:
                        self.current_page = action_param
                        self.pages[action_param].render()

    # Draws the header with the application title, version and optional info
    def draw_header(self, info=None):

        styled_header = self.term.white_on_gray40(
            self.term.center(f"Composr v{app_version}{" - " + info if info else ""}")
        )
        print(self.term.home + styled_header, end="", flush=True)

    # Draws a footer with a label (left) and any information (right) given by parameters
    def draw_footer(self, label: str, info: str):

        with self.term.location(0, self.term.height - 1):

            styled_footer = self.term.white_on_gray40(
                label
                + " " * max(0, self.term.width - len(label) - len(info))
                + info
            )
            print(styled_footer, end="", flush=True)
