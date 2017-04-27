from Ports.AbstractPort import AbstractPort
import IOHelper.config as configIO
import RPi.GPIO as GPIO

class DS1822TemperatureOneWire(AbstractPort):
    """Portklasse für den MCP3008 10-Bit A/D Wandler."""

    homePath = '/sys/bus/w1/devices/'
    exceptFolder = 'w1_bus_master1'

    def __init__(self, settings, id):
        super().__init__(settings, id)
        self.minRefreshTime = 1

        self.nachInit()

    @classmethod
    def getInputs(cls):
        """Gibt die Anschlüsse zurück."""
        import os
        dateiListe = os.listdir(cls.homePath)
        dateiListe.remove(cls.exceptFolder)
        connectors = {}
        if str(cls.__name__) in configIO.loadWiring().keys():
            for ordner in dateiListe:
                connectors['ID:' + ordner] = ordner
            return connectors
        return {}

    def getValueRange(self):
        return [-55, 125, 0.01]

    def getDescription(self):
        return "Port zum Auslesen von DS1820/22 Temperatursensoren über den OneWire Bus. Rückgabewert in °C"

    def isPortInternalOK(self):
        try:
            file = open(self.homePath + self.getInternalPin() + '/w1_slave')
            filecontent = file.read()
            file.close()
            stringvalue = filecontent.split("\n")[1].split(" ")[9]
            temperature = int(stringvalue[2:])
        except:
            return False
        if temperature == 85000: # 85000 ist ein Fehlerwert des DS1822 und sollte nicht als 85 °C interpretiert werden.
            return False
        return True

    def getPrivateState(self):
        """Methode zum Auslesen der Daten."""
        error = 0
        # Es soll maximal 5 mal probiert werden einen Wert zu lesen. Ansonsten wird die Temperatur 0 gesetzt.
        while error < 5:
            try:
                file = open(self.homePath + self.getInternalPin() + '/w1_slave')
                filecontent = file.read()
                file.close()
                stringvalue = filecontent.split("\n")[1].split(" ")[9]
                temperature = float(stringvalue[2:]) / 1000
            except:
                temperature = 0
                error += 1

        return temperature + self.getSetting('offset')