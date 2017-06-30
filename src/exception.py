class ConfigParsingError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class ArgumentParsingError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class ResponseTimeoutError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class ResponseStatusError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
