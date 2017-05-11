from jinja2 import Environment, FileSystemLoader

class AbstactFormField:
    """
    Eine Abstrakte Klasse für Formularfelder. Sie muss vn jeder Klasse implementiert werden die ein Formfeld ist.
    """
    __name = ""
    """Der Name des Formularfeldes"""

    _options = {}
    """Die Optionen des Formularfeldes"""

    _jinjaEnv = None
    """Die Jinjaumgebung des Formularfeldes"""

    _value = None
    """Der aktuelle Wert des Formularfeldes"""

    def __init__(self, name, options):
        self.__name = name
        self.__options = options

        self.__jinjaEnv = Environment(loader=FileSystemLoader(["UI/Templates/FormFields"]))

        if "value" in options.keys():
            self.evaluate(options["value"])
        elif "standard" in options.keys():
            self.evaluate(options["standard"])
        else:
            raise BaseException("Es muss mindestens der Standardwert in den Einstellungen gesetzt werden.")

    def evaluate(self, value):
        """
        Prüft ob der eingegeben Wert in das Formularfeld die Bedingungen erfüllt.
        
        :param value: der Wert der in das Formularfeld eingefüllt werden soll.
        :return: true, wenn der Wert die Bedingungen des Formularfeldes erfüllt.
        """
        internalCheck = self.__evaluate(value)
        blackListCheck = True
        if 'blacklist' in self.__options.keys():
            blackListCheck = not value in self.__options['blacklist']
        return internalCheck and blackListCheck

    def _evaluate(self, value):
        """
        Die von der Kindklasse zu implementierende Evaluate Methode. Sie prüft ob ein Wert zugelassen wird oder nicht.
        
        :param value: der Wert der in das Formularfeld eingefügt werden soll.
        :type value: object
        :return: true, wenn der Wert in dem Formularfeld zulässig ist.
        :rtype: bool
        """
        raise NotImplementedError

    def getHTML(self, updateFormular=False):
        """
        Gibt den HTML Code des Formularfeldes zurück. Muss von der Kindklasse implementiert werden.
        
        :param updateFormular: Gibt an ob es sich ein Formular zum aktualisieren der Daten handelt. In dem Fall wird das Feld als final in der Oberfläche angezeigt.
        :type updateFormular: bool
        :return: Den HTMLCode des Formularfeldes. 
        """
        if updateFormular == True:
            enviroment = Environment(loader=FileSystemLoader("UI/Templates"))
            return enviroment.get_template("finalFormField.html").render(name=self.getName(), value=self.getValue(), displayName=self.getTitle())
        else:
            return self._getHTML()

    def _getHTML(self):
        """
        Gibt den HTML Code des Formularfeldes zurück.
        
        :return: der HTML Code des Formulars
        """
        raise NotImplementedError

    def getName(self):
        """
        Gibt den Namen des Formularfeldes zurück.
        
        :return: den Namen des Formularfeldes
        :rtype: str
        """
        return self.__name

    def getTitle(self):
        """
        Gibt den Titel des Formularfeldes zurück, wie er in er Oberfläche angezeigt werden soll.
                
        :return: der Ttitel des Formularfeldes
        :rtype: str
        """
        return self.__options['name']

    def getDescription(self):
        """
        Gibt die Beschreibung des Formularfeldes zurück, wie sie in der Oberfläche angezeigt erden soll.
        
        :return: die Beschreibung des Formularfeldes
        :rtype: str
        """
        return self.__options['description']

    def getTabIndex(self):
        """
        Gibt den Tabindex des Feldes zurück. Er gibt an an welcher Position das Feld im Formular auftauchen soll.
        
        :return: der Tabindex des Feldes.
        :rtype: int
        """
        if 'tab' in self.__options.keys():
            return self.__options['tab']
        return 0

    def getValue(self):
        """
        Gibt den Wert zurück der im Formularfeld steht. Dies muss immer ein zulässiger Wert sein.
        
        :return: ein zulässiger Wert für das Formularfeld 
        """
        return self._value