# Composr
A terminal UI for building docker compose files

# Developer Information

## Translations

Composr uses Python's `gettext` and Babel for internationalization. English strings are defined directly in the source code using `_()` as the default language. Translations are maintained in `messages.po` and compiled into `messages.mo`.

### Install Babel

```powershell
pip install Babel 
```

### Create and update translations

Run these commands from the project root with Babel installed.

**1. Extract translatable strings from the source code**

```powershell
pybabel extract -o translations/messages.pot src/
```

**2. Initialize a new language** (only once per language):

```powershell
pybabel init -i translations/messages.pot -d translations -l <language-abbrev>
```

**3. Update existing translations** after changing source strings:

```powershell
pybabel update -i translations/messages.pot -d translations
```

**4. Compile translations** after editing `messages.po`:

```powershell
pybabel compile -d translations
```

The compiled translation file is located at `translations/<language-abbrev>/LC_MESSAGES/messages.mo`.

New translatable strings should be wrapped in `_()`, e.g.:

```python
_("Create a new project")
```
