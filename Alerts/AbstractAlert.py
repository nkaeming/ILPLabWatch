from Models.OptionalbeObject import OptionalbeObject


class AbstractAlert(OptionalbeObject):
    """Jeder Alert erbt von dieser Klasse. Jeder Alert ist ein Type der optionierbar vom Benutzer ist."""

    superOptions = {
        "name": {
            "type": "text",
            "tab": -1,
            "name": "Alertbezeichnung",
            "description": "Der Name des Alerts bestehend aus a-z, A-Z und 0-9. Keine Leer- oder Sonderzeichen.",
            "final": True
        },
        "description": {
            "type": "text",
            "tab": 0,
            "name": "Beschreibung",
            "desciption": "Eine Beschribung des Alerts.",
            "length": 200
        }
    }

    alertID = 0  # die eindeutige ID des Alerts

    def __init__(self, alertID, settings):
        settings["type"] = self.getType()
        super().__init__(settings)
        self.alertID = alertID

    # Wird vom Trigger Objekt aufgerufen, wenn der Alert auslösen soll.
    def throwAlert(self, port):
        raise NotImplementedError

    # gibt die Beschreibung des Alerttyps zurück.
    def getDescription(self):
        raise NotImplementedError

    # gibt die Optionen des Alerts zurück. Diese werden dann in der GUI angezeigt. Kann überschrieben werden, sofern nötig.
    def getOptions(self):
        return {**super().getOptions, **self.superOptions}

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
