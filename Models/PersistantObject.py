import json, os


class PersistantObject:
    """
    Klassen die von dieser Klasse erben sind Persistent und können ihre Einstellungen im Konfigurationsordner speichern.
    Diese Möglichkeit sollte von Singeltons wie Services benutzt werden.
    """

    pathToConf = "conf"
    """Der Pfad zum Konfigurationsordner"""

    def writeConf(self, conf):
        """
        Speichert die Konfiguration des Objektes .
        
        :param conf: die Konfiguration des Objektes.
        :type conf: dict
        """
        path = self.pathToConf + "/" + self.getConfigFileName()
        os.makedirs(os.path.dirname(path), 0o0777, True) # wenn die Datei noch nicht existiert wird sie erstellt.
        with open(path, "w") as configfile:
            json.dump(conf, configfile, indent=4)
            configfile.close()

    # gibt den Configfilenamen. Sollte überschrieben werden.
    def getConfigFileName(self):
        """
        Gibt den Dateinamen der Konfigurationsdatei zurück. Sollte normalerweise überschrieben werden.
        
        :return: den Dateinamen der Konfigurationsdatei.
        :rtype: str
        """
        return str(self.__class__.__name__) + ".cfg"

    def getConf(self):
        """
        Lädt die gespeicherte Konfiguration.
        
        :return: die Knfiguration
        :rtype: dict
        """
        conf = {}
        with open(self.pathToConf + "/" + self.getConfigFileName(), "r") as configfile:
            conf = json.load(configfile)
            configfile.close()
        return conf

    def appendMainConfigKey(self, key, settings):
        """
        Fügt in der obersten Ebene einen Mutterknoten für eine Einstellung hinzu.
        
        :param key: der Name des Mutterknotens der Einstellung
        :type key: str
        :param settings: die Einstellungen die unter diesem Muttknoten gespeichert werden sollen.
        :type settings: dict
        """
        conf = self.getConf()
        if not (key in conf.keys()):
            conf[key] = settings
        self.writeConf(conf)
