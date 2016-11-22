from Ports.abstractAlert import abstractAlert


# a command line alert simply prints an alert message on the console.
class commandLineAlert():
    def getDescription(self):
        return "Gibt eine Warnmeldung auf der Konsole aus."

    def throwAlert(self, port):
        print("Der Port " + port.getName() + " hat den kritischen Wert " + str(port.getValue()) + " erreicht.")
