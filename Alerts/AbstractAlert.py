from Models.OptionableObject import OptionableObject


class AbstractAlert(OptionableObject):
    """Jeder Alert erbt von dieser Klasse. Jeder Alert ist ein Type der optionierbar vom Benutzer ist."""

    superOptions = {
        "name": {
            "type": "text",
            "tab": -1,
            "name": "Alertbezeichnung",
            "description": "Der Name des Alerts bestehend aus a-z, A-Z und 0-9. Keine Leer- oder Sonderzeichen.",
            "final": True,
            "required": True,
            "regex": "[A-Za-z0-9]+"
        },
        "description": {
            "type": "text",
            "tab": 0,
            "name": "Beschreibung",
            "description": "Eine Beschreibung des Alerts.",
            "length": 200
        }
    }

    alertID = 0  # die eindeutige ID des Alerts

    def __init__(self, alertID, settings):
        settings["type"] = self.getType()
        super().__init__(settings)
        self.alertID = alertID

    # Wird vom Trigger Objekt aufgerufen, wenn der Alert auslösen soll.
    def throwAlert(self, port, trigger):
        raise NotImplementedError

    # gibt die Beschreibung des Alerttyps zurück.
    def getDescription(self):
        raise NotImplementedError

    # gibt die Optionen des Alerts zurück. Diese werden dann in der GUI angezeigt. Kann überschrieben werden, sofern nötig.
    @classmethod
    def getOptions(cls):
        return {**super().getOptions(), **cls.superOptions}

    # gibt die AlertID zurück.
    def getID(self):
        return self.alertID

    # gibt den Typ des alerts zurück.
    def getType(self):
        return str(self.__class__.__name__)

    # gibt den Namen eines Alerts zurück.
    def getName(self):
        return self.getSetting("name")

    # setzt die Beschreibung des Alerts neu.
    def setDescription(self, description):
        self.setSetting("description", description)

    # Gibt den Namen des Services der die Objekte verwaltet zurück.
    def getServiceName(self):
        return "AlertService"

    def __eq__(self, other):
        """Prüft zwei Alerts auf Gleichheit. Zwei ALerts sind gleich bei gleicher ID und gleichem Typ"""
        if other.__class__ == self.__class__:
            return other.getID() == self.getID()
        return False
