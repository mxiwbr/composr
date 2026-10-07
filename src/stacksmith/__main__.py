from textual.app import App, ComposeResult
from textual.containers import Center, Vertical
from textual.widgets import Static, OptionList, Footer
from textual.widgets._option_list import Option
from textual.widgets import Header

class Stacksmith(App):
    CSS_PATH = "style.tcss"
    def compose(self) -> ComposeResult:
        yield Header(
            show_clock=True
        )
        yield Center(
            OptionList(
                    Option("New"),
                    Option("Quit"),
                    id="menu",
            )
        )
        yield Footer()

if __name__ == "__main__":
    app = Stacksmith()
    app.run()