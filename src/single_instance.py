class SingleInstance(object):
    @classmethod
    def get(cls, name):
        return getattr(cls, name, None)

    @classmethod
    def set(cls, name, value):
        if hasattr(cls, name):
            return getattr(cls, name, None)
        setattr(cls, name, value)

