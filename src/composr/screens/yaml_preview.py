from blessed import Terminal
from pygments import highlight
from pygments.formatters import Terminal256Formatter
from pygments.lexers.data import YamlLexer

from composr.app import App
from composr.models.compose_project import ComposeProject
from composr.models.page_elements import Button, PageElement, NavigatorList, ListButton, Placeholder
from composr.models.screen_types import ScreenTypes
from composr.util.element_management import get_first_selectable_element_id
from composr.util.i18n import _
from composr.util.yaml_convertion import to_yaml


class YamlPreview:

    TYPE = ScreenTypes.DETAIL

    def __init__(self, app):

        self.term = app.term
        self.draw_header = app.draw_header
        self.draw_footer = app.draw_footer

        self.app = app

    def __str__(self):
        return "yaml_preview"

    def render(self):

        yaml_text = to_yaml(self.app.compose_project.to_dict())
        colored_yaml = highlight(yaml_text, YamlLexer(), Terminal256Formatter())

        with self.term.location(0, 2):
            print(self.term.cr + self.term.clear_eos + colored_yaml, end="")

        self.update("header")
        self.update("footer")

    def update(self, region):

        if region == "footer":
            self.draw_footer(_("Controls"), _("[Esc] Exit preview · [Q] Quit"))

        if region == "header":
            self.draw_header(f"{_("File preview")}: {self.app.compose_project.filename}")

    def handle_key(self, key):

        if str(key) == "q":
            return [{"type": "quit"}]
        elif key.name == "KEY_ESCAPE":
            return [
                {
                    "type": "navigate_page",
                    "parameter": "previous_page"
                }
            ]

        self.update("elements")
        return None