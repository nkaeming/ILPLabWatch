from Models.OptionableObject import OptionableObject
from Ports.AbstractPort import AbstractPort
from Models.Trigger import Trigger


class AbstractAlert(OptionableObject):
    """Jeder Alert erbt von dieser Klasse. Jeder Alert ist ein Typ der optionierbar vom Benutzer ist."""

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
    """Einstellungen die jeder Alert haben muss."""

    alertID = 0
    """Die eindeutige ID des Alerts."""

    def __init__(self, alertID, settings):
        """
        Initialisiert den Alert.
        
        :param alertID: die ID des Alerts.
        :type alertID: str
        :param settings: die Einstellungen des Alerts
        :type settings: dict
        """
        settings["type"] = self.getType()
        super().__init__(settings)
        self.alertID = alertID

    def throwAlert(self, port, trigger):
        """
        Methode wird von einem Trigger aufgerufen wenn dieser ausgelöst hat. Muss von der Kindklasse implementiert werden.
        
        :param port: der Port der den Trigger ausgelöst hat
        :type port: AbstractPort
        :param trigger: der Trigger der die Methode aufgerufen hat.
        :type trigger: Trigger
        """
        raise NotImplementedError

    @classmethod
    def getDescription(self):
        """
        Gibt die Beschreibung eines Alerttyps zurück. Muss von der Kindklasse implementiert werden.
        
        :return: Die Beschreibung des Alerttyp.
        :rtype: str
        """
        raise NotImplementedError

    @classmethod
    def getOptions(cls):
        """
        Gibt die Optionen eines Alerttyps zurück. Kann überschrieben werden wenn notwendig.
        
        :return: die Optionen des Alerttyps.
        :rtype: dict
        """
        return {**super().getOptions(), **cls.superOptions}

    def getID(self):
        """
        Gibt die ID des Alerts zurück.
        
        :return: die ID des Alerts
         :rtype: str
        """
        return self.alertID

    def getType(self):
        """
        Gibt den Typ des Alerts zurück.
        
        :return: Klassenname des Alerts.
         :rtype: str
        """
        return str(self.__class__.__name__)

    def getName(self):
        """
        Gibt den Namen eines Alerts zurück.
        
        :return: der Name des Alerts
        :rtype: str
        """
        return self.getSetting("name")

    def setDescription(self, description):
        """
        Setzt die Beschreibung eines Alerts neu
        
        :param description: die neue Beschreibung des Alerts.
        :type description: str
        """
        self.setSetting("description", description)

    def getServiceName(self):
        """
        Gibt den Namen des mit dem Alerts assozierten Services zurück.
        
        :return: der Name des Services
        :rtype: str
        """
        return "AlertService"

    def __eq__(self, other):
        """
        Prüft zwei Alerts auf Gleichheit. Zwei Alerts sind genau dann gleich, wenn sie die gleiche ID und den gleichen Typ haben.
        
        :param other: das Objekt mit dem verglichen werden soll.
        :type other: AbstractAlert
        :return: True, wenn beide Objekte gleich sind.
        :rtype: bool
        """
        if other.__class__ == self.__class__:
            return other.getID() == self.getID()
        return False
