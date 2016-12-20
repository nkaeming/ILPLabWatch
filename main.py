from Services.PortService import PortService
from Services.TriggerService import TriggerService
from Services.AlertService import AlertService
import UI.UIServer as UIApp
from bottle import run

AS = AlertService()
PS = PortService()
TS = TriggerService(PS, AS)

run(UIApp)
