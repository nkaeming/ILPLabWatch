import inspect, importlib, os
import IOHelper.config as configIO
from Models.Observable import Observable


class OptionalbeObject(Observable):
    """Klassen die von dieser Klasse erben können Optionen in der im gleichen Ordner angelegten Options.cfg haben. Das bedeutet, dass Objekte dieser Klassen durch die UI Eingestellt werden können."""

    settings = {}  # die vorgenommenen Einstellungen.

    def __init__(self, settings):
        self.settings = settings

    # gibt die Einstellungen des Objektes als dict zurück.
    def getSettings(self):
        return self.settings

    # gibt eine Einstellung zurück.
    def getSetting(self, name):
        if name in self.getSettings().keys():
            return self.getSettings()[name]
        else:
            return ""

    # gibt die Optionen der Klasse zurück. Diese werden dann in der GUI angezeigt. Kann überschrieben werden, sofern nötig.
    def getOptions(self):
        configLink = os.path.dirname(str(inspect.getfile(self.__class__))) + "/options.cfg"
        if os.path.isfile(configLink):
            options = configIO.loadConfig(configLink)
        else:
            options = {}
        return options

    # setzt eine Einstellun mit dem Namen auf die Value value.
    def setSetting(self, name, value):
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
        return ""
