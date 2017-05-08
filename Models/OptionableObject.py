import inspect, importlib, os
import IOHelper.config as configIO
from Models.Observable import Observable


class OptionableObject(Observable):
    """Klassen die diese Klasse erweitern können durch Optionen eingestellt werden.
    Sie müssen dazu im selben Modulordner wie die Kalsse selbst eine Datei mit dem Namen options.cfg enthalten.
    Ports und Alerts sind OptionableObjects. Besonders sinnvoll ist der Einsatz von OptionableObjects, wenn gewünscht ist, dass diese
    über die Oberfläche einstellbar sein sollen. Objekte können mit der Funktion getSetting auf die Einstellungen zurückgreifen.
    """

    settings = {}
    """Die Einstellungen die vorgenommen wurden."""

    def __init__(self, settings):
        self.settings = settings

    def getSettings(self):
        """
        Gibt die Einstellungen des Objektes zurück.
        
        :return: Einstellungen des Objekts.
        :rtype: dict
        """
        return self.settings

    # gibt eine Einstellung zurück.
    def getSetting(self, name):
        """
        Gibt den Wert einer Einstellung zurück. Ist eine Einstellung nicht definiert, so wird versucht den Standardwert zu benutzen.
        Sollte es keinen Standardwert geben wird ein IndexError geworfen.
        
        :param name: der Name der Einstellung
        :type name: str
        :return: die Einstellung
        :rtype: str, float
        """
        if name in self.getSettings().keys():
            return self.getSettings()[name]
        elif name in self.getOptions().keys() and 'standard' in self.getOptions()[name].keys():
            return self.getOptions()[name]['standard']
            raise IndexError("Setting not defined.")

    @classmethod
    def getOptions(cls):
        """
        Gibt die möglichen Optionen einer Klasse zurück.
        
        :return: die Optionen der Klasse
        :rtype: dict
        """
        configLink = os.path.dirname(str(inspect.getfile(cls))) + "/options.cfg"
        if os.path.isfile(configLink):
            options = configIO.loadConfig(configLink)
        else:
            options = {}
        return options

    def setSetting(self, name, value):
        """
        Setzt eine Einstellung neu.
        
        :param name: der Name der Einstellung
        :type name: str
        :param value: der Wert den die Einstelung bekommen soll.
        :type value: str, float, int
        """
        self.settings[name] = value
        if self.getServiceName() != "":
            try:
                serviceClass = getattr(importlib.import_module("Services." + self.getServiceName()),
                                       self.getServiceName())
                self.informObserverOfType(serviceClass)
            except:
                pass

    # wenn das Objekt zu einem Service gehört, so muss der Service bei Änderungen informiert werden. Gibt diese Funktion einen Servicenamen zurück, so wird dieser informiert.
    def getServiceName(self):
        """
        Objekte die von einem Service verwaltet werden müssen kenntlich machen zu welchem Service sie gehören. Nur dann wird beim Ändern einer Einstellung dieser korrekt informiert.
        
        :return: den Namen der Serviceklasse
        :rtype: str
        """
        return ""
