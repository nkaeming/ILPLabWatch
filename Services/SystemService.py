from threading import Thread
import time
#TODO: Service Notwendigkeit überprüfen?? Erfüllt dieser Service einen zweck?
class SystemServiceThread(Thread):
    """Service zum überprüfen des aktuellen Systemstatus. Er muss als eigener Thread gestartet werden, da er nur so den Systemthread prüfen kann."""

    portService = None
    """Der PortService der im System verwendet wird."""
    triggerService = None
    """Der Triggerservice der im System verwendet wird."""
    alertService = None
    """Der Alertservice der im System verwendet wird."""
    uiServer = None
    """Der UI-Server der im System verwendet wird."""

    def __init__(self, PS, TS, AS, UI):
        """
        Initialisierung des Threads und Dependencyinjektion. Ruft automatisch die __init__ der Threadklasse auf.
        
        :param PS: der Portservice
        :param TS: der Triggerservice
        :param AS: der Alertservice
        :param UI: der UI-Server
        """

        self.portService = PS
        self.triggerService = TS
        self.alertService = AS
        self.uiServer = UI
        super().__init__()

    def run(self):
        while True:

            time.sleep(1)

    def check(self):
        """
        Prüft den aktuellen Systemzustand. Gibt False zurück, wenn das System nicht mehr ordentlich funktioniert.
        
        :return: True, wenn der Systemzustand in Ordnung ist.
        """
        if len(self.PortService.getInterruptPorts()) != 0:
            return False
