import json, os


class PersistantObject:
    """Ein PersistantObject ist ein Objekt, welches sich im config Ordner speichern kann."""
    pathToConf = "conf"  # der Pfad zum Konfigurationsordner

    persistantConfig = {}  # die Einsetllungen die gespeichert werden sollen.

    def saveObjectConf(self):
        path = self.pathToConf + "/" + self.getConfigFileName()
        os.makedirs(os.path.dirname(path), 0o0777, True)
        with open(path, "w") as configfile:
            json.dump(self.persistantConfig, configfile, indent=4)
            configfile.close()

    # gibt den Configfilenamen. Sollte überschrieben werden.
    def getConfigFileName(self):
        return str(self.__class__) + ".cfg"

    # lädt die gespeicherte Konfiguration
    def loadObjectConf(self):
        with open(self.pathToConf + "/" + self.getConfigFileName(), "r") as configfile:
            self.persistantConfig = json.load(configfile)
            configfile.close()
        self.setUp()

    # wird aufgerufen, wenn die ObjectConf eingeladen wurde.
    def setUp(self):
        raise NotImplementedError
