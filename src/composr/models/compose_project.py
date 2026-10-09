class ComposeProject:
    def __init__(self, name=None):
        self.data = {
            **({"name": name} if name else {}),
            "services": {},
        }