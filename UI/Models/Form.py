from jinja2 import Environment, FileSystemLoader
from UI.Models.FormFieldFactory import FormFieldFactory

class Form:
    """
    Objekte der Klasse Form bilden Formulare in der Benutzeroberfläche ab.
    """

    __fields = []
    """Eine Liste mit allen Formfeldern."""

    __method = ""
    """Entweder POST oder GET"""

    __action = ""
    """Link zur Auswertung der Seite."""

    __buttonText = ""
    """Der Text der auf dem Submitbutton stehen soll."""

    def __init__(self, options, action, buttonText="Speichern", method="GET"):
        self.__method = method
        self.__action = action
        self.__buttonText = buttonText

        for name, option in options.items():
            self.__fields.append(FormFieldFactory.makeNewFormField(name, option))

    def addFormField(self, FormField):
        """
        Fügt dem Formular ein Formfeld hinzu. Der Name des Formfeldes muss eindeutig sein. Andernfalls wird ein Fehler geworfen.
        
        :param FormField: Das Formfeld welches hinzugefügt werden soll.
        :type FormField: AbstractFormField
        """
        if not self.doesFormFieldNameExist(FormField.getName()):
            self.__fields.append(FormField)
        else:
            raise EnvironmentError("Ein Formular kann nicht zwei Felder gleichen Namens enthalten.")

    def doesFormFieldNameExist(self, name):
        """
        Prüft ob der Name eines Formfeldes enthalten ist.
        
        :param name: der Name des Formfeldes. 
        :return: true, wenn der Name bereits vergeben ist.
        """
        return len(filter(lambda formField: formField.getName() == name, self.__fields)) >= 1

    def getHTML(self):
        """
        Gibt den HTML-Code des Formulars zurück.
        
        :return: 
        """
        jinjaEnv = Environment(
            loader=FileSystemLoader(["UI/Templates"]))

        template = jinjaEnv.get_template("form.html")
        return template.render(method = self.__method, action=self.__action,
                                    formFields = sorted(self.__fields, key=lambda formField: formField.getTabIndex()),
                                    buttonText = self.__buttonText)

    def evaluate(self, inputs):
        """
        Prüft ob die Eingabe eines Formulars korrekt war. Nach ausführen dieser Methode kann getHTML dazu benutzt werden das Formular erneut mit Hinweisen auszugeben.
        
        :param inputs: Die Eingabe die Überprüft werden soll. Ist ein Dictionary mit den Feldnamen als Schlüssel und den Werten als Elementen. 
        :type inputs: dict
        :return: true, wenn die das Formular korrekt ausgefüllt wurde.
        :rtype: bool
        """
        for formField in self.__fields:
            if formField.getName() in inputs.keys():
                formField.evaluate(input[formField.getName()])
            else:
                formField.evaluate(None)

        return len(filter(lambda formField: formField.correctFilled() == True, self.__fields)) == 0