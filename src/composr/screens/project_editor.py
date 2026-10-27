from blessed import Terminal

from composr.models.compose_project import ComposeProject
from composr.models.page_elements import Button, PageElement
from composr.util.i18n import _

class ProjectEditor:

    compose_project: ComposeProject | None
    elements: list[PageElement]
    focused: str | None
    edit: str | None

    def __init__(self, term: Terminal, draw_header, draw_footer, app):

        self.term = term
        self.draw_header = draw_header
        self.draw_footer = draw_footer

        self.app = app

        self.reset()

    def reset(self):

        self.compose_project = None

        self.elements = [
            Button(
                _("Back"),
                [
                    {
                        "type": "navigate_page",
                        "parameter": "previous_page"
                    }
                ]
            )
        ]

        self.focused = self.elements[0].get_id()
        self.edit = None

    def __str__(self):
        return "project_editor"

    def render(self):

        self.compose_project = self.app.compose_project

        print(self.term.clear + self.term.home, end="")

        self.draw_header(self.compose_project.get_name())
        self.compose_project.write()

        self.update("elements")
        self.update("footer")

    def update(self, region):

        if region == "elements":

            last_element = None

            with self.term.location(0, 2):
                for element in self.elements:

                    style = self.term.black_on_silver if self.focused == element.get_id() else self.term.normal

                    if isinstance(element, Button):

                        label = (self.term.bold + element.get_label() + self.term.normal) if self.focused != element.get_id() else element.get_label()
                        option_text = f"[ {style}{label}{self.term.normal} ]"

                        if last_element == "Button":
                            print(f"\t{option_text}", end="")
                        else:
                            print(f"\n{self.term.cr + self.term.clear_eol + option_text}", end="")

                        last_element = element.get_type()

        elif region == "footer":
            if self.edit is None:
                self.draw_footer(_("Controls"), _("[↑][↓] Navigate · [Enter] Select · [Q] Quit"))
            else:
                self.draw_footer(_("Controls"), _("[Enter] Confirm changes"))

    def handle_key(self, key):

        element = next(element for element in self.elements if element.get_id() == self.focused)

        match key.name:
            case "KEY_ENTER":
                if isinstance(element, Button):
                    return element.get_actions()

        self.update("elements")
        return None