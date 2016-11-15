#the provided function are used for the configuration input and output.
import json

#TODO: Not working well.

#reads a conf file
def readConf(confLink):
    with open(confLink, "r") as configfile:
        conf = json.load(configfile)
        return conf

#write a conf file.
def writeConf(confLink, config):
    with open(confLink, "w") as configfile:
        json.dump(config, configfile, indent=4)

#reads the port conf
def readPortConf():
    return readConf("portsConf.cfg")

#write the ports conf
def writePortConf(config):
    writeConf("portsConf.cfg", config)

#reads the wiring conf
def readWiringConf():
    return readConf("wiringConf.cfg")


