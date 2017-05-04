"""Die Datei die zum Starten des Porgamms mit root Rechten ausgeführt werden muss."""
from Services.PortService import PortService
from Services.TriggerService import TriggerService
from Services.AlertService import AlertService
from UI.UIServer import UIServer
from statusLED import LEDThread
import os

IP = '0.0.0.0'
"""Die IP-Adresse des Sockets auf die das System gesetzt werden soll."""

if __name__ == '__main__':
    # Setzen der Umgebungspfade.
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    # Service Initialisierung.
    AS = AlertService()
    PS = PortService()
    TS = TriggerService(PS, AS)
    AS.setTriggerService(TS)
    PS.setTriggerService(TS)

    # Überwachungs LED's initialisieren.
    LED = LEDThread(PS)
    LED.start()

    # Server für die Oberfläche starten
    server = UIServer(PS, TS, AS)
    server.start(IP)