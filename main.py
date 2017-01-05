from Services.PortService import PortService
from Services.TriggerService import TriggerService
from Services.AlertService import AlertService
from UI.UIServer import UIServer

if __name__ == '__main__':
    AS = AlertService()
    PS = PortService()
    TS = TriggerService(PS, AS)

    server = UIServer(PS, TS, AS)
    server.start()