from composr.app import App
from composr.util import i18n

i18n.set_lang("auto")

while True:
    app = App()
    if app.run() != 1:
        break