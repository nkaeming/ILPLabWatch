class Observer():
    """Objekte dieser Klasse können Objekte des Typen Observable beobachten."""

    def observableChanged(self, observable):
        raise NotImplementedError
