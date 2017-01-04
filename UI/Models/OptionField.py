from jinja2 import FileSystemLoader, Environment
import re

class OptionField:
    """Diese Klasse repräsentiert die Optionsfelder die in den Ports und Alerts eingestellt sind. Sie konvertiert die Typen zu den im System u.Ä."""

    name = ""
    settings = {}
    warnText = ""
    jinjaEnv = None
    value = ""
    template = None

    def __init__(self, name, settings, value="", warnText=""):
        """settings sind die Einstellung zu der Option, der Name ist der ursprüngliche key im dict."""
        self.name = name
        self.settings = settings
        self.warnText = warnText

        # prüfen ob ein Standardwert geladen werden soll.
        if value == "":
            if 'standard' in settings.keys():
                self.value = settings['standard']
            else:
                self.value = ""
        else:
            self.value = value

        # prüft ob es eine Beschreibung geben soll
        if not 'description' in settings.keys():
            self.settings['description'] = ""

        # prüft ob die Eingabe des Wertes notwendig ist.
        if not 'required' in settings.keys():
            self.settings['required'] = False

        if not 'tab' in settings.keys():
            self.settings['tab'] = 0

        self.jinjaEnv = Environment(loader=FileSystemLoader(["UI/Templates/Forms"]))
        self.prepare()

    def prepare(self):
        """Bereitet das Optionsfeld vor."""
        inType = self.settings['type']
        settingKeys = self.settings.keys()
        if inType == 'text':
            if not 'length' in settingKeys:
                self.settings['length'] = 20

            template = self.jinjaEnv.get_template('FormsTextInput.html')
        elif inType == 'number':
            if not 'min' in settingKeys:
                self.settings['min'] = 0
            if not 'max' in settingKeys:
                self.settings['max'] = 100
            if not 'resolution' in settingKeys:
                self.settings['resolution'] = 1

            # typ konvertierung.
            if isinstance(self.value, str):
                self.value = float(self.value)
                if self.value % 1 == 0:
                    self.value = int(self.value)
            elif not isinstance(self.value, (int, float)):
                raise TypeError


            template = self.jinjaEnv.get_template('FormsNumberInput.html')
        elif inType == 'boolean':
            template = self.jinjaEnv.get_template('FormsCheckboxInput.html')
            # Konvertiere Wert nach Boolean
            if self.value in ('on', True, 1, 'True', 'true', '1'):
                self.value = True
            else:
                self.value = False

        elif inType == 'select':
            template = self.jinjaEnv.get_template('FormsSelectInput.html')
        else:
            template = self.jinjaEnv.get_template('FormsType404.html')
        self.template = template

    def getHtml(self):
        """Gibt den HTML Code für dieses Formelement zurück."""
        return self.template.render(settings=self.settings, value=self.value, warnText=self.warnText,
                                    name=self.name)

    def getTabIndex(self):
        """Gibt den Tabindex des Formelements zurück."""
        if not 'tab' in self.settings.keys():
            return 0
        else:
            return self.settings['tab']

    def evaluate(self):
        """Prüft ob die value der Option gegen die Standardtests zulässig ist."""
        type = self.settings['type']
        ok = True
        if type == 'text':
            # die zulässige Länge überprüfen
            if len(self.value) > self.settings['length']:
                self.warnText += " Die zulässige Zeichenanzahl wurde überschritten."
                ok = False

            # die optionale regex überprüfung durchführen
            if 'regex' in self.settings.keys():
                if re.fullmatch(self.settings['regex'], self.value) == None:
                    self.warnText += " Der Text stimmt nicht mit den Bedingungen überein. (Regular Expression was: " + \
                                     self.settings['regex'] + ")"
                    ok = False
        elif type == 'number':
            # prüfen ob der Wert im Wertebereich liegt.
            if not (float(self.value) >= float(self.settings['min']) and float(self.value) <= float(
                    self.settings['max'])):
                self.warnText += " Der Wert liegt außerhalb des zugelassenden Bereichs von " + self.settings[
                    'min'] + " bis " + self.settings['max']
                ok = False
            # Prüfen ob der Wert durch die Auflösung aufgelöst werden kann
            if not (float(self.value) % float(self.settings['resolution']) == 0):
                self.warnText += " Der Wert entspricht nicht der zugelassenden Auflösung von " + self.settings[
                    'resolution'] + "."
                ok = False
        self.warnText = self.warnText.strip()
        return ok

    def getName(self):
        return self.name

    def getValue(self):
        return self.value
