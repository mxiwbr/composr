import sys
from blessed import Terminal
import importlib.metadata

term = Terminal()
app_version = importlib.metadata.version("stacksmith")

# Draws the header with the application title and version as well as a clock in 24hr format to the top of the screen
def draw_header(title):

    styled_header = term.white_on_gray40(
        term.center(title)
    )
    print(term.home + styled_header, end="", flush=True)

# Draws a footer with controls overview to the bottom of the screen
def draw_footer():

    with term.location(0, term.height - 1):

        controls = "↑↓ move, Enter select, q quit "
        label = " Controls"

        styled_footer = term.white_on_gray40(
            label
            + " " * max(0, term.width - len(label) - len(controls))
            + controls
        )
        print(styled_footer, end="", flush=True)

# Renders and controls the start menu
def render_start_menu():

    selection = 0
    menu_options = [
        "Create new compose file",
        "Quit"
    ]

    print(term.clear + term.home, end="")

    while True:

        draw_header(f"Stacksmith v{app_version}")
        draw_footer()

        print(
            term.move_y(1)
            + "\nWelcome to Stacksmith!\n"
            + term.darkgray
            + "A terminal application for building docker compose files\n"
            + term.normal
        )

        # Print the options
        for i, option in enumerate(menu_options):
            print(f"{term.cr + term.clear_eol}{">" if selection == i else ""} {option}")

        # Obtain the pressed key and it's string
        key = term.inkey()
        key_str = str(key)

        if key.name == "KEY_UP":
            selection = max(0, selection - 1)
        elif key.name == "KEY_DOWN":
            selection = min(max(0, len(menu_options) - 1), selection + 1)
        elif key.name == "KEY_ENTER" or key_str == "\n":
            if selection == 1:
                sys.exit(0)
        elif key_str == "q":
            sys.exit(0)

with term.fullscreen(), term.cbreak(), term.hidden_cursor():
    while True:
        render_start_menu()