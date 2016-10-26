#this adapter can be used for working with conf Files. All conf files are keept up to date by this functions
import ConfModule.confReader as confReader

#adds a new port to the configuration
#name: the display name of the port, port: the port on the connector Box, logged: True or False, loginterval: the loginterval in secondes
def addPort(name, port, logged, loginterval):
    #Todo: implement
    return 0

#gets the port information of all ports.
def getPortsConf():
    return confReader.readPortConf()["ports"]

#gets the internal Number of an external Port.
def getInternalPort(externalPort):
    return confReader.readWiringConf()[str(externalPort)]

#returns the configuration of one port by the external Port number
def getPortConf(externalPort):
    return confReader.readPortConf()["ports"][str(externalPort)]