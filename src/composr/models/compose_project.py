class ComposeProject:
    def __init__(self, filename, name = None):
        self.data = {
            **({"name": name} if name else {}),
            "services": {},
        }
        self.filename = filename

    def get_name(self):
        return self.data["name"]

    def get_filename(self):
        return self.filename