# This File forkes the two main processes for the deamons. One is the webDeaon and the other is the logDeamon
# TODO: Deamons fork
from Deamons.webDeamon import WebDeamon
from Ports.portService import portService

from old.Deamons.loggerDeamon import LoggerDeamon

if __name__ == "__main__":
    PS = portService()

    webDemaon = WebDeamon(PS)
    loggerDeamon = LoggerDeamon(PS)

    webDemaon.start()
    loggerDeamon.start()

    while True:
        if webDemaon.isAlive == False:
            print("Der Webdeamon ist abgestürzt.")
        if loggerDeamon.isAlive == False:
            print("Der Logger ist abgestürzt.")
