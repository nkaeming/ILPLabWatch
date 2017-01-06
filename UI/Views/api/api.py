from UI.AbstractView import AbstractView
import cherrypy, json, datetime
import IOHelper.log as Logreader


class api(AbstractView):
    """Die API Klasse stellt Funktionen zur Verwalltung für Fremdsoftware zur Verfügung."""

    def __init__(self, PortService, TriggerService, AlertService):
        super().__init__(PortService, TriggerService, AlertService)

    @cherrypy.expose
    def currentStatus(self, portName=""):
        """Gibt den aktuellen Status aller Ports zurück."""
        if portName == "":
            return json.dumps(self.PortService.getCurrentPortsInformations())
        else:
            return json.dumps(self.PortService.getPortByName(portName).getCurrentInformations())

    @cherrypy.expose
    def getLog(self, portName="", portID="", type="json", startDate="", endDate=""):
        """Gibt die Logdaten im angegebenden Zeitraum zurück. Zulässige typen sind json"""
        # TODO: Mehr typen hinzufügen
        if portName == "" and portID == "":
            raise cherrypy.HTTPError(400, "Es muss entweder portName oder portID spezifiziert werden.")

        # setze die passenden start und end Daten.
        if startDate == "":
            startDate = datetime.datetime.now() + datetime.timedelta(days=-1)
        else:
            startDate = datetime.datetime.fromtimestamp(float(startDate))

        if endDate == "":
            endDate = datetime.datetime.now()
        else:
            endDate = datetime.datetime.fromtimestamp(float(endDate))

        # prüfen ob das Startdatum zulässig ist.
        if startDate > endDate:
            raise cherrypy.HTTPError(400, "Das Startdatum darf nicht nach dem Enddatum liegen.")

        # entscheide ob er port nach seiner ID oder seinem Namen geholt werden soll.
        if portName == "":
            port = self.PortService.getPortByID(portID)
        else:
            port = self.PortService.getPortByName(portName)

        # daten je nach Typ auslesen.
        data = Logreader.readLog(port, startDate, endDate)

        if type == "json":
            return json.dumps(data)
