class Observable():
    """Erbt eine Klasse von Observable, so kann sie von Observern beobachtet werden."""
    observers = []

    # Fügt einen neuen Observer (Beobachter) hinzu.
    def addObserver(self, observer):
        if not (observer in self.observers):
            self.observers.append(observer)

    # Entfernt einen Observer
    def removeObserver(self, observer):
        self.observers.remove(observer)

    # informiert alle Observer über eine Änderung
    def informObserver(self):
        for observer in self.observers:
            observer.observableChanged(self)
