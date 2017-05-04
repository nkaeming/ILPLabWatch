class Observer():
    """
    Objekte dieser Klasse können Objekte des Typen Observable beobachten.
    """

    def observableChanged(self, observable):
        """
        Wird vom Observable aufgerufen wen es sich veränert hat. Muss von der Kindklasse implementiert werden.
        
        :param observable: die veränerte Observable
        :type observable: Observable
        """
        raise NotImplementedError
