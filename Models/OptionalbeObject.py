import inspect
import os
import IOHelper.config as configIO


class OptionalbeObject:
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
