class Observable():
    """
    Observable ist eine der zwei abstrakten Klassen die zur Implementation des Beobachtermusters notwendig ist.
    Erbt eine Klasse von Observable, so kann sie von Observern beobachtet werden.
    """
    observers = []

    # Fügt einen neuen Observer (Beobachter) hinzu.
    def addObserver(self, observer):
        """
        Fügt dem Observable einen Beobacter hinzu. Dieser wird informiert, sobald sich am Observable etwas entscheidenes ändert.
        
        :param observer: Das Beobachterobjekt welches beobachten soll.. 
        :type observer: Observer
        """
        if not (observer in self.observers):
            self.observers.append(observer)

    def removeObserver(self, observer):
        """
        Entfernt einen Observer.
        
        :param observer: der Observer der entfernt werden soll.
        :type observer: Observer
        """
        self.observers.remove(observer)

    def removeAllObservers(self):
        """
        Entfernt alle Observer
        """
        for observer in self.observers:
            self.removeObserver(observer)

    # informiert alle Observer über eine Änderung
    def informObserver(self):
        """
        Diese Methode wird vom Kindobjekt aufgerufen, wenn sich etwas verändert hat. Es werden dann die Observer benachrichtigt.
        """
        for observer in self.observers:
            observer.observableChanged(self)

    def informObserverOfType(self, type):
        """
        Informiert alle Observer eines bestimmten Typs. Ist im klassischen Beobachtermuster nicht vorgesehen aber besonders in Pyton ziemlich nützlich
        
        :param type: der Typ der zu informierenden Observer 
        """
        observers = list(filter(lambda object: isinstance(object, type), self.observers))
        for observer in observers:
            observer.observableChanged(self)
