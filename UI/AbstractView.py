class AbstractView():
    """Erstellt einige Grundfunktionen zu einem View. Jeder View muss diese Klasse erweitern"""

    PortService = None
    TriggerService = None
    AlertService = None

    """DependencyInjection für die Services."""

    def __init__(self, PortService, TriggerService, AlertService):
        self.PortService = PortService
        self.AlertService = AlertService
        self.TriggerService = TriggerService
