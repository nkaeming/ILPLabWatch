from Ports.AbstractPort import AbstractPort
import Adafruit_DHT

class DHT11New(AbstractPort):
    def __init__(self, settings, id):
        super().__init__(settings, id)
        self.minRefreshTime = 4
        self.afterInit()

    def getPrivateState(self):
        """Gibt den aktuellen State des Ports zurück."""
        return

    def getPrivateState(self):
        """Gibt den aktuellen State des Ports zurück."""
        sensor = Adafruit_DHT.DHT11
        pin = self.getInternalPin()
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        return temperature

    def getValueRange(self):
        return [0, 100, 0.2]

    def getDescription(self):
        return "Port zum auslesen der Luftfeuchtigkeit in % vom DHT11"