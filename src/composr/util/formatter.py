def format_port(port: int | tuple[int, int]) -> str:
    if isinstance(port, int):
        return str(port)
    elif isinstance(port, tuple):
        return f"{port[0]}-{port[1]}"
    else:
        return ""