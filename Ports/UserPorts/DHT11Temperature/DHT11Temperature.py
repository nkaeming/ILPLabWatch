from Ports.AbstractPort import AbstractPort
import Adafruit_DHT

class DHT11Temperature(AbstractPort):
    """Portklasse für den DHT11"""

    def __init__(self, settings, id):
        super().__init__(settings, id)
        self.minRefreshTime = 5
        self.nachInit()

    def getValueRange(self):
        return [-55, 100, 0.5]

    def getDescription(self):
        return "Port zum auslesen der Temperatur in °C vom DHT11"

    def getPrivateState(self):
        """Methode zum Auslesen der Daten."""
        sensor = Adafruit_DHT.DHT11
        pin = self.getInternalPin()
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        return temperature