from Services.PortService import PortService
from Services.TriggerAlertService import TriggerService

PS = PortService()
TS = TriggerService(PS)
PS.setTriggerService(TS)

# trigger = TS.addTrigger(50, 52, PS.getPortByName("Bla"), True)
# alert = TS.addAlert("CommandLineAlert", {"name": "Toll", "description":"Whuppp"})
# TS.addAlertTriggerRelation(trigger, alert)
print("Blubber")
# print(TS.getTriggerOfPort(PS.getPortByName("Bla")))
