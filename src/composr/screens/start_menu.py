from blessed import Terminal

from composr.models.page_elements import ListButton
from composr.util.i18n import _

class StartMenu:
    def __init__(self, term: Terminal, draw_header, draw_footer):

        self.term = term
        self.draw_header = draw_header
        self.draw_footer = draw_footer

        self.elements = [
            ListButton(
                _("New project") + "\n",
                [{
                    "type": "navigate_page",
                    "parameter": "create_project"
                }]
            ),
            ListButton(
                _("Settings"),
                [{
                    "type": "navigate_page",
                    "parameter": "settings"
                }]
            ),
            ListButton(
                _("Quit"),
                [{
                    "type": "quit"
                }]
            ),
        ]

        self.focused = self.elements[0].get_id()

    def __str__(self):
        return "start_menu"

    def render(self):

        print(self.term.clear + self.term.home, end="")

        self.draw_header()
        self.draw_footer(_("Controls"), _("[↑][↓] Navigate · [Enter] Select · [Q] Quit"))

        with self.term.location(0, 1):
            print(
                self.term.bold
                + "\n"
                + _("Welcome to Composr!")
                + "\n"
                + self.term.normal
                + self.term.darkgray
                + _("A terminal application for building docker compose files.")[:self.term.width - 1]
                + "\n"
                + self.term.normal
            )

        self.update("elements")

    def update(self, region):
        if region == "elements":

            with self.term.location(0, 5):
                for element in self.elements:
                    print(f"{self.term.cr + self.term.clear_eol + self.term.bold}{">" if self.focused == element.get_id() else self.term.normal} {element.get_label() + self.term.normal}")

    def handle_key(self, key):

        element = next(element for element in self.elements if element.get_id() == self.focused)

        match key.name:
            case "KEY_DOWN":

                elements = iter(self.elements)
                next(element for element in elements if element.get_id() == self.focused)
                self.focused = next(elements, self.elements[0]).get_id()

            case "KEY_UP":

                elements = reversed(self.elements)
                next(element for element in elements if element.get_id() == self.focused)
                self.focused = next(elements, self.elements[-1]).get_id()

            case "KEY_ENTER":

                if isinstance(element, ListButton):
                    return element.get_actions()

            case _:
                if str(key) == "\n":
                    if isinstance(element, ListButton):
                        return element.get_actions()
                elif str(key) == "q":
                    return [{ "type": "quit" }]

        self.update("elements")
        return None