import json, os


class PersistantObject:
    """Ein PersistantObject ist ein Objekt, welches sich im config Ordner speichern kann."""
    pathToConf = "conf"  # der Pfad zum Konfigurationsordner

    # speichert die konfiguration des objekts.
    def writeConf(self, conf):
        path = self.pathToConf + "/" + self.getConfigFileName()
        os.makedirs(os.path.dirname(path), 0o0777, True)
        with open(path, "w") as configfile:
            json.dump(conf, configfile, indent=4)
            configfile.close()

    # gibt den Configfilenamen. Sollte überschrieben werden.
    def getConfigFileName(self):
        return str(self.__class__.__name__) + ".cfg"

    # lädt die gespeicherte Konfiguration
    def getConf(self):
        conf = {}
        with open(self.pathToConf + "/" + self.getConfigFileName(), "r") as configfile:
            conf = json.load(configfile)
            configfile.close()
        return conf

    # wird aufgerufen, wenn die ObjectConf eingeladen wurde.
    def setUp(self):
        raise NotImplementedError

    # fügt in der obersten ebene einen Key mit den Einstellungen hinzu.
    def appendMainConfigKey(self, key, settings):
        conf = self.getConf()
        if not (key in conf.keys()):
            conf[key] = settings
        self.writeConf(conf)
