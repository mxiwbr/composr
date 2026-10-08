from blessed import Terminal

term = Terminal()

def draw_header(title):
    header_text = term.center(title)
    styled_header = term.white_on_gray40(header_text)
    print(term.clear + term.move_xy(0, 0) + styled_header, end="", flush=True)

with term.fullscreen(), term.cbreak(), term.hidden_cursor():
    while True:
        draw_header("Stacksmith")