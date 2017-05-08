from Models.Observer import Observer
from Models.Observable import Observable

class Trigger(Observer, Observable):
    """
    Trigger sind ein wesentlicher Bestandteil des Systems. Sie sind die Verbindung zwischen den Alerts und den Ports.
    Ein Trigger wird immer informiert, wenn sich der Wert eines Ports verändert hat. Er prüft dann, ob dieser Wert innerhalb der gewählten Grenzen zum Auslösen liegt.
    Ist dies der Fall, so werden alle Alerts informiert, die mit dem Trigger verbunden sind. Die strickte Trenung zwischen Alerts und Ports
    durch Trigger erlaubt es so eine 1 zu n Relation zwischen Ports und Alerts herzustellen.
    """

    triggerRange = [0,
                    0]
    """Der Bereich in dem der Trigger auslösen soll. Die erste Zahl ist das Minimum und die zweite Zahl das Maximum."""

    port = None
    """Die Instanz des Ports mit dem der Trigger verknüpft ist,"""

    alerts = []
    """Eine Liste mit Alertinstanzen, die informiert werden sollen, wenn der Trigger auslöst."""

    warnTrigger = False
    """Legt fest pb es sich um einen WarnTrigger handelt. Ist diese Einstellung True, so gibt es einen optischen Indikator für das Auslösen."""

    triggerID = 0
    """Die Eindeutige TriggerID"""

    # min ist die untere Schranke des Triggers und max die obere.
    def __init__(self, triggerID, minimal, maximal, port, warnTrigger):
        """
        Erzeugt einen neuen Trigger.
        
        :param triggerID: die eindeutige ID des Triggers
        :type triggerID: str
        :param minimal: die unter Schranke ab der der Trigger auslösen soll.
        :type minimal: float
        :param maximal: die obere Schranke bis die der Trigger auslösen soll.
        :type maximal: float
        :param port: die Instanz des Ports mit der ein Trigger verbunden ist.
        :type port: AbstractPort
        :param warnTrigger: die Einstellung ob es sich um einen WarnTrigger handelt.
        :type warnTrigger: bool
        """
        self.alerts = []
        self.triggerRange = [minimal, maximal]
        self.port = port
        self.triggerID = triggerID
        self.port.addObserver(self)
        self.warnTrigger = warnTrigger

    def observableChanged(self, observable):
        """
        Von Observer geerbt. Wird ausgelöst, wenn sich das Portobjekt verändert hat.
        
        :param observable: die Instanz die sich verändert hat. (wird ier nicht benötigt.)
        """
        self.checkAndCall()

    def checkAndCall(self):
        """
        Prüft ob der Wert des Port innerhalb der Grenzen liegt und uft dann alle Alerts auf. Sollte generell aufgerufen werden.
        
        """
        if self.check():
            self.callAlerts()

    def check(self):
        """
        Prüft ob der aktuelle Wert des Ports innerhalb der Grenzen liegt.
        
        :return: true, wenn der aktuelle Wert innerhalb der Grenzen liegt.
        :rtype: bool
        """
        return self.checkValue(self.port.getState())

    def checkValue(self, value):
        """
        Prüft ob ein bestimmter Wert den Trigger auslösen würde. Informiert jedoch nicht die Alerts.
        
        :param value: der Wert der überprüft werden soll.
        :type value: float
        :return: true, wenn der Wert den Trigger auslösen würde.
        :rtype: bool
        """
        return self.triggerRange[0] <= value and value <= self.triggerRange[1]

    def callAlerts(self):
        """
        Löst alle Alerts aus.
        """
        for alert in self.alerts:
            alert.throwAlert(self.port, self)

    def isFirstCalled(self):
        """
        Gibt true zurück, wenn der Trigger zum ersten Mal ausgelöst wurde. D.h. wenn der Wert zum ersten Mal in den Bereich reingelaufen ist.
        
        :return: true, wenn der Trigger zum ersten Mal ausgelöst wurde.
        :rtype: bool
        """
        portHistory = self.port.getPortHistory()
        if self.checkValue(portHistory[-1]) == True:
            return False
        return True

    def getMinimalValue(self):
        """
        Gibt den minimalen Wert zurück, bei dem der Trigger auslöst.
        
        :return: die untere Schrnake des bereiches bei dem der Trigger auslöst.
        :rtype: float
        """
        return self.triggerRange[0]

    def getMaximalValue(self):
        """
        Gibt den maximalen Wert zurück, bei dem der Trigger auslöst.

        :return: die obere Schrnake des bereiches bei dem der Trigger auslöst.
        :rtype: float
        """
        return self.triggerRange[1]

    # fügt ein neues alert Objekt hinzu.
    def appendAlert(self, alert):
        """
        Fügt dem Trigger einen neuen Alert hinzu. Der Alert wird dann beim nächsten Aus lösen des Triggers informiert.
        
        :param alert: Der Alert der hinzugefügt werden soll.
        :type alert: AbstractAlert
        """
        self.alerts.append(alert)
        self.informTriggerService()

    def informTriggerService(self):
        """
        Private Methode um den Triggerservice zu informieren
        """
        from Services.TriggerService import TriggerService
        self.informObserverOfType(TriggerService)

    # gibt true zurück, wenn der Trigger als Warnung im UI auftauchen soll.
    def isWarnTrigger(self):
        """
        Gibt true zurück, wenn der Trigger als Warnung  im UI auftauchen soll.
        
        :return: warnTrigger
        :rtype: bool
        """
        return self.warnTrigger

    def getPort(self):
        """
        Gibt die Instanz des Ports zurück der den Trigger auslöst.
        
        :return: den Port den der Trigger auslöst.
        :rtype: AbstractPort
        """
        return self.port

    def getID(self):
        """
        Getter
        
        :return: die ID des Trigger
        :rtype: str
        """
        return self.triggerID

    def getAlerts(self):
        """
        Gibt alle Alerts zurück mit denen der Trigger verbunden ist.
        
        :return: Eine Liste aller Alerts.
        :rtype: list
        """
        return self.alerts

    def removeAlert(self, alert):
        """
        Entfernt einen Alert vom Trigger.
        
        :param alert: Der Alert der entfernt werden soll.
        :type alert: AbstractAlert
        """
        if alert in self.alerts:
            self.alerts.remove(alert)
            from Services.TriggerService import TriggerService
            self.informObserverOfType(TriggerService)

    def getSettings(self):
        """
        Gibt die Einstellungen des Triggers zurück.
        
        :return: die Einstellugen des Triggers
        :rtype: dict
        """
        conf = {}
        conf["portID"] = self.getPort().getID()
        conf["warnTrigger"] = self.isWarnTrigger()
        conf["range"] = self.triggerRange

        alertList = []
        for alert in self.getAlerts():
            alertList.append(alert.getID())
        conf["alerts"] = alertList

        return conf

    def setWarntrigger(self, value):
        """
        Legt fest ob ein Trigger ein Warntrigger ist oder nicht.
        
        :param value: true, wenn der Trigger ein Warntrigger werden soll.
        :type value: bool
        """
        self.warnTrigger = value
        self.informTriggerService()

    def setInterval(self, value):
        """
        Stellt das Intervall ein in dem der Trigger auslösen soll.
        
        :param value: Ein Tupel aus dem minimalen und maximalen Wert. (Minimum, Maximum)
        :type value: tuple 
        """
        self.triggerRange = value
        self.informTriggerService()

    def __eq__(self, other):
        """
        Prüft ob zwei Trigger gleich sind. Zwei Trigger sind genau dann gleich, wenn ihre ID übereinstimmt.
        
        :param other: das zu vergleichende Objekt.
        :type other: object
        :return: true, wenn es sich um den gleichen Trigger handelt, false sonst.
        :rtype: bool
        """
        if self.__class__ == other.__class__:
            if self.getID() == other.getID():
                return True
        return False
