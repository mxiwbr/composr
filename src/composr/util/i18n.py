import gettext
import locale
from pathlib import Path

LOCALE_DIR = Path(__file__).resolve().parents[3] / "translations"
_selected_lang = None
_translation = gettext.NullTranslations()

def setup_i18n():
    global _translation

    lang = _selected_lang or locale.getlocale()[0] or "en"
    lang = lang.split(".")[0].replace("-", "_")

    _translation = gettext.translation(
        "messages",
        localedir=LOCALE_DIR,
        languages=[lang, lang.split("_")[0]],
        fallback=True
    )

def set_lang(lang: str):

    global _selected_lang
    _selected_lang = lang
    setup_i18n()

def get_avl_langs() -> list[tuple[str, str]]:

    languages = []

    for lang_dir in sorted(LOCALE_DIR.iterdir()):

        mo_file = lang_dir / "LC_MESSAGES" / "messages.mo"

        if not mo_file.is_file():
            continue

        with mo_file.open("rb") as file:
            catalog = gettext.GNUTranslations(file)

        display_name = catalog.pgettext("metadata", "language-display-name")
        if display_name == "language-display-name":
            display_name = lang_dir.name

        languages.append((lang_dir.name, display_name))

    return languages

def _(message: str) -> str:
    return _translation.gettext(message)

setup_i18n()