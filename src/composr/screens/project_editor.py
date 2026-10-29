from composr.models.compose_project import ComposeProject
from composr.models.page_elements import Button, PageElement, NavigatorList, ListButton, Placeholder
from composr.models.screen_types import ScreenTypes
from composr.util.element_management import get_first_selectable_element_id
from composr.util.i18n import _

class ProjectEditor:

    compose_project: ComposeProject | None
    elements: list[PageElement]
    focused: str | None
    edit: str | None

    TYPE = ScreenTypes.MAIN

    def __init__(self, app):

        self.term = app.term
        self.draw_header = app.draw_header
        self.draw_footer = app.draw_footer

        self.app = app

    def reset(self):

        self.elements = [
            NavigatorList(
                _("Services"),
                _("No services added yet."),
                self.app.compose_project.get_services(),
                0
            ),
            Placeholder(
                Placeholder.PlaceholderType.LINE
            ),
            ListButton(
                _("Add service"),
                [
                    {
                        "type": "suspend_previous_page_save",
                        "parameter": ""
                    },
                    {
                        "type": "navigate_page",
                        "parameter": "service_editor",
                        "page_parameter": None
                    }
                ]
            ),
            Button(
                _("Back"),
                [
                    {
                        "type": "navigate_page",
                        "parameter": "previous_page"
                    }
                ]
            ),
            Button(
                _("Preview"),
                [
                    {
                        "type": "navigate_page",
                        "parameter": "yaml_preview"
                    }
                ]
            )
        ]

        self.focused = get_first_selectable_element_id(self.elements)
        self.edit = None

    def __str__(self):
        return "project_editor"

    def render(self):

        self.reset()

        print(self.term.clear + self.term.home, end="")

        self.draw_header(self.app.compose_project.get_name())
        self.app.compose_project.write()

        self.update("elements")
        self.update("footer")

    def update(self, region):

        if region == "elements":

            last_element = None

            with self.term.location(0, 2):
                for element in self.elements:

                    style = self.term.black_on_silver if self.focused == element.get_id() else self.term.normal

                    if isinstance(element, ListButton):

                        print(f"{self.term.cr + self.term.clear_eol + self.term.bold}{">" if self.focused == element.get_id() else self.term.normal} {element.get_label() + self.term.normal}")

                    elif isinstance(element, Placeholder):

                        print(element.get_label(), end="")

                    elif isinstance(element, Button):

                        label = (self.term.bold + element.get_label() + self.term.normal) if self.focused != element.get_id() else element.get_label()
                        item_text = f"[ {style}{label}{self.term.normal} ]"

                        if last_element == "Button":
                            print(f"\t{item_text}", end="")
                        else:
                            print(f"\n{self.term.cr + self.term.clear_eol + item_text}", end="")

                        last_element = element.get_type()

                    elif isinstance(element, NavigatorList):

                        label = self.term.bold + element.get_label() + self.term.normal

                        print(label, end="\n\n")

                        if element.is_empty():
                            print(element.empty_message)
                        else:
                            for item in element.get_items():
                                print(f"{self.term.cr + self.term.clear_eol + self.term.bold}{">" if element.get_selected() == item and element.get_id() == self.focused else self.term.normal} {item[1].name + self.term.normal}")

        elif region == "footer":
            if self.edit is None:
                self.draw_footer(_("Controls"), _("[↑][↓] Navigate · [Enter] Select · [Q] Quit"))
            else:
                self.draw_footer(_("Controls"), _("[Enter] Confirm changes"))

    def handle_key(self, key):

        element = next(element for element in self.elements if element.get_id() == self.focused)

        match key.name:
            case "KEY_ENTER":
                if isinstance(element, Button) or isinstance(element, ListButton):
                    return element.get_actions()

                elif isinstance(element, NavigatorList):
                    return element.get_actions()

            case "KEY_DOWN":

                elements = iter(self.elements)

                if isinstance(element, NavigatorList):
                    if not element.move_selection(1):
                        next(element for element in elements if element.get_id() == self.focused)
                        self.focused = next((e for e in elements if e.is_selectable()), self.elements[0]).get_id()
                else:
                    next(element for element in elements if element.get_id() == self.focused)
                    self.focused = next((e for e in elements if e.is_selectable()), self.elements[0]).get_id()

            case "KEY_UP":

                elements = reversed(self.elements)

                if isinstance(element, NavigatorList):
                    if not element.move_selection(-1):
                        next(element for element in elements if element.get_id() == self.focused)
                        self.focused = next((e for e in elements if e.is_selectable()), self.elements[-1]).get_id()
                else:
                    next(element for element in elements if element.get_id() == self.focused)
                    self.focused = next((e for e in elements if e.is_selectable()), self.elements[-1]).get_id()

            case _:
                if str(key) == "\n" and isinstance(element, Button):
                    return element.get_actions()
                elif str(key) == "q":
                    return [{"type": "quit"}]

        self.update("elements")
        return None