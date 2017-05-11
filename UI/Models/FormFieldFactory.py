import importlib

class FormFieldFactory():
    """
    Eine Factory Klasse zum erzeugen neuer Formfelder.
    """

    @classmethod
    def makeNewFormField(cls, name, options):
        """
        Erzeugt ein neues Formualrfeld je nach Typ.
        
        :param name: der Name des Formfeldes
        :type name: str
        :param options: die Optionen des Formfeldes
        :type options: dict
        :param unallowedEntries: eine Liste verbotener Einträge für das Formfeld.
        :type unallowedEntries: list
        :return: das Formfeld.
        :rtype: AbstractFormField
        """
        if not 'type' in options:
            raise NotImplementedError("Der Porttyp der in den Einstellungen angegeben wurde existiert nicht.")
        else:
            type = str(options['type'])
            classPointer = getattr(importlib.import_module("UI.Models.FormFields." + type + "." + type), type)
            return classPointer(name, options)
