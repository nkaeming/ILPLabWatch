from Services.PortService import PortService
from Services.TriggerService import TriggerService
from Services.AlertService import AlertService

AS = AlertService()
PS = PortService()
TS = TriggerService(PS, AS)
