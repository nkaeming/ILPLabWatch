from Services.PortService import PortService
from Services.TriggerService import TriggerService
from Services.AlertService import AlertService
from UI.UIServer import UIServer
from Services.SystemService import SystemServiceThread

if __name__ == '__main__':
    AS = AlertService()
    PS = PortService()
    TS = TriggerService(PS, AS)
    AS.setTriggerService(TS)
    PS.setTriggerService(TS)

    server = UIServer(PS, TS, AS)
    server.start()