from jinja2 import FileSystemLoader, Environment


class OptionField:
    """Diese Klasse repräsentiert die Optionsfelder die in den Ports und Alerts eingestellt sind."""

    name = ""
    settings = {}
    warnText = ""
    jinjaEnv = None
    value = ""

    """settings sind die Einstellung zu der Option, der Name ist der ursprüngliche key im dict."""

    def __init__(self, name, settings, value="", warnText=""):
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

    def getHtml(self):
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

            template = self.jinjaEnv.get_template('FormsNumberInput.html')
        elif inType == 'boolean':
            template = self.jinjaEnv.get_template('FormsCheckboxInput.html')
        else:
            template = self.jinjaEnv.get_template('FormsType404.html')

        return template.render(settings=self.settings, value=self.value, warnText=self.warnText, name=self.name)

    def getTabIndex(self):
        if not 'tab' in self.settings.keys():
            return 0
        else:
            return self.settings['tab']
