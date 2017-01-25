from Ports.AbstractPort import AbstractPort
import IOHelper.config as configIO
import RPi.GPIO as GPIO

class MCP3008AnalogToDigital(AbstractPort):
    """Portklasse für den MCP3008 10-Bit A/D Wandler."""

    wandlerID = "" # Dient zur Unterscheidung der verschiedenen Wandler, sofern mehrere angeschlossen sind.
    adPin = 0 # der Anschlusspin am AD Wandler.
    CLK = 18 # Ist bei jedem Wandler gleich.
    DIN = 0 # Digitaler Input Kanal
    DOUT = 0 # Digitaler Output Kanal
    CS = 0 # Chip Select Kanal

    def __init__(self, settings, id):
        super().__init__(settings, id)
        self.wandlerID = self.getInternalPin().split("-")[0]
        self.minRefreshTime = self.getSetting("timeResolution") * 1/1000
        self.setUpConnection()
        self.nachInit()

    def setUpConnection(self):
        """Initialiserit die GPIO-Ports."""
        GPIO.setmode(GPIO.BCM)
        # Lade die Chipeinstellungen aus der Configdatei
        wiring = configIO.loadWiring()[self.__class__.__name__][self.wandlerID]
        self.CLK = wiring["CLK"]
        self.DIN = wiring["DIN"]
        self.DOUT = wiring["DOUT"]
        self.CS = wiring["CS"]
        # Pin Programmierung
        GPIO.setup(self.CLK, GPIO.OUT)
        GPIO.setup(self.DIN, GPIO.OUT)
        GPIO.setup(self.DOUT, GPIO.IN)
        GPIO.setup(self.CS, GPIO.OUT)

    @classmethod
    def getInputs(cls):
        """Gibt die Anschlüsse zurück."""
        connectors = {}
        wiring = configIO.loadWiring()[str(cls.__name__)]
        for wandler in wiring.keys():
            for i in range(1,9):
                connectors["Wandler:" + str(wandler) + " Anschluss: " + str(i)] = str(wandler) + "-" + str(i)
        return connectors

    def getValueRange(self):
        linearFaktor = self.getSetting("linearScalar")
        return [1*linearFaktor, 1024*linearFaktor, 1]

    def getDescription(self):
        return "Ein Port zum Auslesen der Daten eines MCP3008 10-bit A/D Wandlers."

    def getPrivateState(self):
        """Methode zum Auslesen der Analogen Daten."""
        # Pegel setzen
        HIGH = True
        LOW = False
        # Pegel definieren
        GPIO.output(self.CS, HIGH)
        GPIO.output(self.CS, LOW)
        GPIO.output(self.CLK, LOW)

        cmd = self.adPin
        cmd |= 0b00011000  # Kommando zum Abruf der Analogwerte des Datenkanals adCh

        # Bitfolge senden
        for i in range(5):
            if (cmd & 0x10):  # 4. Bit prüfen und mit 0 anfangen
                GPIO.output(self.DIN, HIGH)
            else:
                GPIO.output(self.DIN, LOW)
            # Clocksignal negative Flanke erzeugen
            GPIO.output(self.CLK, HIGH)
            GPIO.output(self.CLK, LOW)
            cmd <<= 1  # Bitfolge eine Position nach links verschieben

        # Datenabruf
        adchvalue = 0  # Wert auf 0 zurücksetzen
        for i in range(11):
            GPIO.output(self.CLK, HIGH)
            GPIO.output(self.CLK, LOW)
            adchvalue <<= 1  # 1 Postition nach links schieben
            if (GPIO.input(self.DOUT)):
                adchvalue |= 0x01
        return adchvalue * self.getSetting("linearScalar")