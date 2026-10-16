from blessed import Terminal

from composr.models.page_elements import Button, CycleButton, PageElement
from composr.util import i18n
from composr.util.i18n import _, get_avl_langs, set_lang

class Settings:

    elements: list[PageElement]
    focused: str | None
    edit: str | None
    confirm: bool

    def __init__(self, term: Terminal, draw_header, draw_footer):

        self.term = term
        self.draw_header = draw_header
        self.draw_footer = draw_footer

        self.reset()

    def reset(self):

        self.elements = [
            CycleButton(
                _("Language"),
                [
                    ("auto", "Auto"),
                    ("en", "English"),
                    *get_avl_langs()
                ],
                i18n.get_selected_lang()
            ),
            Button(
                _("Back"),
                [{
                    "type": "navigate_page",
                    "parameter": "previous_page"
                }]
            )
        ]

        self.focused = self.elements[0].get_id()
        self.edit = None
        self.confirm = False

    def __str__(self):
        return "settings"

    def render(self):

        print(self.term.clear + self.term.home, end="")

        self.confirm = False

        self.draw_header(_("Settings"))
        self.draw_footer(_("Controls"), _("[↑][↓] Navigate · [Enter] Select · [Q] Quit"))

        self.update("elements")

    def update(self, region):

        if region == "elements":

            last_element = None

            with self.term.location(0, 2):
                for element in self.elements:

                    style = self.term.black_on_silver if self.focused == element.get_id() else self.term.normal

                    # cycle button (edit mode)
                    if isinstance(element, CycleButton) and self.edit == element.get_id():

                        self.focused = None
                        style = self.term.normal

                        label = self.term.bold + element.get_label() + self.term.normal
                        option_text = f"{label}: {self.term.bold}<{self.term.normal} {style}{element.get_selected()[1]}{self.term.normal} {self.term.bold}>{self.term.normal}"

                        print(f"{self.term.cr + self.term.clear_eol + option_text}")

                        last_element = element.get_type()

                    # cycle button
                    elif isinstance(element, CycleButton):

                        label = self.term.bold + element.get_label() + self.term.normal
                        option_text = f"{label}: {style}{element.get_selected()[1]}{self.term.normal}"

                        print(f"{self.term.cr + self.term.clear_eol + option_text}")

                        last_element = element.get_selected()[1]

                    # buttons
                    elif isinstance(element, Button):

                        label = (self.term.bold + element.get_label() + self.term.normal) if self.focused != element.get_id() else element.get_label()
                        option_text = f"[ {style}{label}{self.term.normal} ]"

                        if last_element == "Button":
                            print(f"\t{option_text}", end="")
                        else:
                            print(f"\n{self.term.cr + self.term.clear_eol + option_text}", end="")

                        last_element = element.get_type()

        elif region == "footer":

            if self.confirm:
                self.draw_footer(_("Restart is required to apply this setting."), _("[Enter] Confirm · [Esc] Cancel"), "confirm")

            elif self.edit is not None:
                self.draw_footer(_("Controls"), _("[←][→] Navigate options · [Enter] Confirm changes · [Esc] Cancel"))

            else:
                self.draw_footer(_("Controls"), _("[↑][↓] Navigate · [Enter] Select · [Q] Quit"))

    def handle_key(self, key):

        if self.edit is None:

            element = next(element for element in self.elements if element.get_id() == self.focused)

            match key.name:
                case "KEY_ENTER":

                    if isinstance(element, Button):
                        return element.get_actions()

                    elif isinstance(element, CycleButton):
                        self.edit = element.get_id()
                        self.update("footer")

                case "KEY_DOWN":

                    elements = iter(self.elements)
                    next(element for element in elements if element.get_id() == self.focused)
                    self.focused = next(elements, self.elements[0]).get_id()

                case "KEY_UP":

                    elements = reversed(self.elements)
                    next(element for element in elements if element.get_id() == self.focused)
                    self.focused = next(elements, self.elements[-1]).get_id()

                case _:
                    if str(key) == "\n" and isinstance(element, Button):
                        return element.get_actions()
                    elif str(key) == "q":
                        return [{"type": "quit"}]
        else:

            element = next(element for element in self.elements if element.get_id() == self.edit)

            match key.name:
                case "KEY_ENTER":

                    if isinstance(element, CycleButton) and self.confirm is True:

                        set_lang(element.get_selected()[0])

                        self.focused = self.edit
                        self.edit = None
                        self.update("footer")

                        return [{"type": "reload"}]

                    elif isinstance(element, CycleButton) and element.changed:

                        self.confirm = True
                        self.update("footer")

                    elif isinstance(element, CycleButton):

                        self.focused = self.edit
                        self.edit = None
                        self.update("footer")

                case "KEY_ESCAPE":

                    if isinstance(element, CycleButton):

                        self.focused = self.edit
                        self.edit = None
                        self.confirm = False

                        element.select_option(i18n.get_selected_lang())
                        element.changed = False

                        self.update("footer")

                case "KEY_RIGHT":

                    if isinstance(element, CycleButton):

                        element.move_selection(1)

                        if element.get_selected()[0] != i18n.get_selected_lang():
                            element.changed = True
                        else:
                            element.changed = False

                        self.confirm = False
                        self.update("footer")

                case "KEY_LEFT":

                    if isinstance(element, CycleButton):
                        element.move_selection(-1)

                        if element.get_selected()[0] != i18n.get_selected_lang():
                            element.changed = True
                        else:
                            element.changed = False

                        self.confirm = False
                        self.update("footer")

                case _:

                    if str(key) == "\n":
                        self.focused = self.edit
                        self.edit = None
                        self.update("footer")

        self.update("elements")
        return None