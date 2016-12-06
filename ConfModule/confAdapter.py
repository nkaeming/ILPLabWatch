#this adapter can be used for working with conf Files. All conf files are keept up to date by this functions
import ConfModule.confReader as confReader
import uuid

#adds a new port to the configuration
#name: the display name of the port, port: the port on the connector Box, logged: True or False, loginterval: the loginterval in secondes
def addPort(port):
    portConf = confReader.readPortConf()
    portConf[port.getExternalPort()] = port.getSettings()
    confReader.writePortConf(portConf)

#gets the port information of all ports.
def getPortsConf():
    return confReader.readPortConf()

#gets the internal Number of an external Port. nedds also the type of the port.
def getInternalPort(type, externalPort):
    return confReader.readWiringConf()[type][str(externalPort)]

#returns all ports of a type.
def getInternalPorts(type):
    try:
        return confReader.readWiringConf()[type]
    except:
        return {}

# updates the port in the wiring conf
def updateWiringConf(type, conf):
    oldConf = confReader.readWiringConf()
    oldConf[type].pop()
    oldConf[type] = conf
    confReader.writeWiringConf(oldConf)

#returns the configuration of one port by the external Port number
def getPortConf(externalPort):
    return confReader.readPortConf()[str(externalPort)]

# returns the trigger conf.
def getTriggersOf(portName):
    try:
        return confReader.readTriggerConf()[portName]
    except:
        return {}

# returns the whole trigger conf
def getTriggerConf():
    return confReader.readTriggerConf()

# adds a new trigger to the conf. alerts is in the form of {"alertType": settingsDic, "2ndAlertType": setingsDic}
def addTrigger(portName, alerts, min, max):
    confTriggers = getTriggersOf(portName)
    id = str(uuid.uuid4())
    confTriggers[id]["range"] = [min, max]
    confTriggers[id]["alerts"] = alerts
    bigConf = confReader.readTriggerConf()
    bigConf[portName] = confTriggers
    confReader.writeTriggerConf(bigConf)

# updates a trigger with the trigger id
def updateTrigger(triggerID, alerts, min, max):
    raise NotImplementedError
    #TODO: implement.