import json, codecs, os

wiringConf = "conf/wiringConf.cfg"
"""
Speicherort der Verbindungseinstellungen
"""

def loadWiring():
    """
    Gibt die Verbindungseinstellungen zurück.
    
    :return: die Verbindungseinstellungen
    :rtype: dict
    """
    return loadConfig(wiringConf)

def loadConfig(configLink):
    """
    Lädt eine Einstellungsdatei
    
    :param configLink: der Pfad zur Einstellungsdatei
    :type configLink: str
    :return: die Einstellungen
    :rtype: dict
    """
    with open(configLink, "r", encoding='utf-8') as configfile:
        conf = json.load(configfile)
        return conf

def saveConfig(configLink, content):
    """
    Speichert die Einstellungen in einer Datei
    
    :param configLink: er Pfad zur Einstellungsdatei
    :param content: 
    :return: 
    """
    with open(configLink, "w", encoding='utf-8') as configfile:
        json.dump(content, configfile, indent=4)
