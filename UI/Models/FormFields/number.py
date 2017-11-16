from UI.Models.AbstractFormField import AbstactFormField

class number(AbstactFormField):

    __errorMessages = []
    """Fehlermedlungen die bei falschen Eingaben angezeigt werden sollen."""

    __minimum = 0
    __maximum = 100
    __resolution = 1

    def __init__(self, name, options):
        super().__init__(name, options)
        if "min" in options.keys():
            self.__minimum = options["min"]
        if "max" in options.keys():
            self.__maximum = options["max"]
        if "resolution" in options.keys():
            self.__resolution = options["resolution"]

    def _getHTML(self):
        """
        Gibt den HTML-Code des Formularfeldes zurück.
        :return: der HTML-Code des Formularfeldes.
        """
        self._jinjaEnv.getTemplate("number.html")

    def _evaluate(self, value):
        """
        Prüft ob eine Eingabe in das Feld korrekt ist. Dazu muss zunächst der Typ der Eingabe stimmen. Zulässig sind int, float und Strings der Form "1.1" oder "1,1"
        Zusätzlich muss der eingegebene Werte innerhalb des zulässigen Wertebereichs liegen.
        
        :param value: der Wert der in das Formularfeld gesetzt werden soll.
        :type value: str, float, int
        :return: true, wenn der Wert in dem Formularfeld zulässig ist.
        :rtype: bool
        """
        if type(value) == int or type(value) == float:
            cleanValue = value
        elif type(value) == str:
            if value.find(",") != -1:
                value.replace(",", ".")
            if value.find(".") == -1:
                try:
                    cleanValue = int(value)
                except:
                    self.__errorMessages.append("Der übermittelte Wert wird von diesem Eingabefeld nicht akzeptiert.")
            else:
                try:
                    cleanValue = float(value)
                except:
                    self.__errorMessages.append("Der übermittelte Wert wird von diesem Eingabefeld nicht akzeptiert.")

        else:
            self.__errorMessages.append("Der übermittelte Wert wird von diesem Eingabefeld nicht akzeptiert.")


