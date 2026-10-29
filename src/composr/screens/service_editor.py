from composr.models import service
from composr.models.page_elements import PageElement, Button
from composr.models.screen_types import ScreenTypes
from composr.util import element_management
from composr.util.i18n import _

class ServiceEditor:

    elements: list[PageElement]
    focused: str | None
    edit: str | None
    # The index of the service in the compose project's service array OR None, indicating service creation mode
    service: int | None

    TYPE = ScreenTypes.DETAIL

    def __init__(self, app):
        self.term = app.term
        self.draw_header = app.draw_header
        self.draw_footer = app.draw_footer

        self.app = app

    def render(self, svc: int | None = None):
        self.service = svc

        if self.service is not None:
            self.service = self.app.compose_project.services[self.service]

        self.reset()

        print(self.term.clear + self.term.home, end="")

        self.draw_header(f"{self.app.compose_project.get_name()} - {_("Add service") if not isinstance(self.service, service.Service) else _("Edit service") + " " + self.term.yellow_on_gray40 + self.service.name + self.term.normal}")

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

    def reset(self):

        self.elements = [
            Button(
                _("Cancel"),
                [{
                    "type": "navigate_page",
                    "parameter": "project_editor"
                }]
            ),
            Button(
                _("Save"),
                [
                    "save_service"
                ]
            )
        ]

        self.focused = element_management.get_first_selectable_element_id(self.elements)
        self.edit = None

    def __str__(self):
        return "service_editor"

    def handle_key(self, key):

        element = next(element for element in self.elements if element.get_id() == self.focused)

        match key.name:

            case "KEY_ENTER":
                if isinstance(element, Button):
                    return element.get_actions()

            case "KEY_DOWN":
                elements = iter(self.elements)
                next(element for element in elements if element.get_id() == self.focused)
                self.focused = next((e for e in elements if e.is_selectable()), self.elements[0]).get_id()

            case "KEY_UP":
                elements = reversed(self.elements)
                next(element for element in elements if element.get_id() == self.focused)
                self.focused = next((e for e in elements if e.is_selectable()), self.elements[-1]).get_id()

            case _:
                if str(key) == "q":
                    return [{"type": "quit"}]

        self.update("elements")
        return None