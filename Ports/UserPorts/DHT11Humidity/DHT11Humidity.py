from Ports.AbstractPort import AbstractPort
import Adafruit_DHT

class DHT11Humidity(AbstractPort):
    """Portklasse für den DHT11"""

    def __init__(self, settings, id):
        super().__init__(settings, id)
        self.minRefreshTime = 5
        self.nachInit()

    def getValueRange(self):
        return [0, 100, 0.2]

    def getDescription(self):
        return "Port zum auslesen der Luftfeuchtigkeit in % vom DHT11"

    def getPrivateState(self):
        """Methode zum Auslesen der Daten."""
        sensor = Adafruit_DHT.DHT11
        pin = self.getInternalPin()
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        return humidity