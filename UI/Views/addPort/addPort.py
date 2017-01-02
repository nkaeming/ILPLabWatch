from UI.AbstractView import AbstractView


class addPort(AbstractView):
    """View zum erstellen neuer Ports."""

    def __init__(self, PS, TS, AS):
        super().__init__(PS, TS, AS)
