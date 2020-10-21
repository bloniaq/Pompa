class Variable():
    """
    """

    def __init__(self, value):
        self.value = None
        self.callbacks = {}

    def add_callback(self, func):
        self.callbacks[func] = None

    def _callbacks(self):
        for func in self.callbacks:
            func(self.value)

    def set(self, value):
        self.value = value
        self._callbacks()

    def get(self):
        return self.value


class FloatVariable(Variable):
    """
    """

    def __init__(self):
        pass
