from urllib.parse import parse_qsl, urlparse
# this file defines a few helper functions to deal with the URL

# returns the HTTP-Request Get informations of an URL
def getGetInormations(rqURL):
    getString = urlparse(rqURL).query
    gets = dict((x,y) for x, y in parse_qsl(getString))
    return gets


# vergleicht die get Informationen der Anfrage mit einem Dictionary von Optionen und konvertiert die Eingaben zu ensprechenden Typen in Python.
# existiert eine get Information in dem angegebenen optionen nicht, so wird diese auf den standard Wert gesetzt.
def convertGetInformations(rqURL, options):
    gets = getGetInormations(rqURL)
    results = {}
    for key, value in options.items():
        if key in gets.keys():
            getValue = gets[key]
            if value["type"] == "number":
                if "." in getValue:
                    results[key] = float(getValue)
                else:
                    results[key] = int(getValue)
            elif value["type"] == "boolean":
                if str.lower(getValue) == "on" or str.lower(getValue) == "yes" or str.lower(getValue) == "true":
                    results[key] = True
                else:
                    results[key] = False
            elif value["type"] == "text":
                results[key] = str(getValue)
        else:
            results[key] = options[key]["standard"]
    return results

# returns the module on the number no. Example getModule(www.example.com/abc/def/ghj, 2) returns def
def getSubUrl(rqURL, no):
    try:
        part = rqURL.split("/")[no]
    except:
        part = ""
    if "?" in part:
        return part.split("?")[0]
    return part


# returns the Module of an URL
def getModule(rqURL):
    return getSubUrl(rqURL, 1)


# returns the Submodule if setted
def getSubmodule(rqURL):
    return getSubUrl(rqURL, 2)
