from Services.PortService import PortService
from Services.TriggerService import TriggerService
from Services.AlertService import AlertService
from UI.UIServer import UIServer
from statusLED import LEDThread
import os

if __name__ == '__main__':
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    AS = AlertService()
    PS = PortService()
    TS = TriggerService(PS, AS)
    AS.setTriggerService(TS)
    PS.setTriggerService(TS)

    LED = LEDThread(PS)
    LED.start()

    server = UIServer(PS, TS, AS)
    server.start()