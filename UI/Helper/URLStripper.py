#this file defines a few helper functions to deal with the URL

#returns the HTTP-Request Get informations of an URL
def getGetInormations(rqURL):
    gets = {}
    rqURL = rqURL.split("/")
    getString = rqURL[-1].split("?")[1]
    for keyvalue in getString.split("&"):
        keyvalue = keyvalue.split("=")
        gets[keyvalue[0]] = keyvalue[1]
    return gets

#returns the Module of an URL
def getModule(rqURL):
    return rqURL.split("/")[1]

#returns the Submodule if setted
def getSubmodule(rqURL):
    part = rqURL.split("/")[-1]
    if "?" in part:
        return part.split("?")[0]
    return part