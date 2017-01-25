from threading import Thread
import time

class SystemServiceThread(Thread):
    """Service zum überprüfen des aktuellen Systemstatus."""
    portService = None
    triggerService = None
    alertService = None
    uiServer = None

    def __init__(self, PS, TS, AS, UI):
        self.portService = PS
        self.triggerService = TS
        self.alertService = AS
        self.uiServer = UI
        super().__init__()

    def run(self):
        while True:

            time.sleep(1)

    def check(self):
        """Prüft den aktuellen Systemzustand. Gibt False zurück, wenn das System nicht mehr ordentlich funktioniert."""
        if len(self.PortService.getInterruptPorts()) != 0:
            return False
