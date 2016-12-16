from Models.OptionalbeObject import OptionalbeObject


class AbstractAlert(OptionalbeObject):
    """Jeder Alert erbt von dieser Klasse. Jeder Alert ist ein Type der optionierbar vom Benutzer ist."""

    def __init__(self, settings):
        super().__init__(settings)

    # Wird vom Trigger Objekt aufgerufen, wenn der Alert auslösen soll.
    def throwAlert(self, port):
        raise NotImplementedError
