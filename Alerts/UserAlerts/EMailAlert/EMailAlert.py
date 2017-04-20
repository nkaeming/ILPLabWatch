from Alerts.AbstractAlert import AbstractAlert
import datetime, smtplib

class EMailAlert(AbstractAlert):
    """Diese Klasse gibt eine Nachricht auf der Konsole aus, sobald der Alert aufgerufen wird."""

    lastCalled = 0

    def __init__(self, alertID, settings):
        super().__init__(alertID, settings)

    # erzeugt einen neuen Alert in der Command Line.
    def throwAlert(self, port, trigger):
        td = datetime.timedelta(minutes=-5)
        if self.lastCalled < datetime.datetime.now() + td:
            smtp = smtplib.SMTP()
            smtp.connect(host=self.getSetting('SMTPServerAddress'), port=self.getSetting('SMTPServerPort'))
            if self.getSetting('SMTPUsername') != "":
                smtp.login(user=self.getSetting('SMTPUsername'), password=self.getSetting('SMTPPassword'))

            for address in self.getSetting('sendTo').split(';'):
                to = address.strip()
                self.sendMail(to, port, smtp)
            self.lastCalled = datetime.datetime.now()

    # gibt die Beschreibung des Alerts aus.
    def getDescription(self):
        return "Ein E-Mail-Alert sendet eine E-Mail an einen oder mehre Empfänger, wenn der Trigger das erste Mal auslöst."

    def sendMail(self, to, port, smtp):
        """Sendet eine Email an einen Empfänger"""

        message = """From: ILPLabWatch <noReply@ILPLabWatch.uni-hamburg.de>
        To: {} <{}>
        Subject: ILPLabWatch Alert ausgelöst

        Alert vom Port {} ausgelöst \n
        Der Wert vom Port betrug: {} \n
        Zusätzliche Nachricht: {} \n
        Zeitpunkt: {}
        """

        message = message.format(to, to, port.getName(), port.getStateWithUnit(), self.getSetting('message'), datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S"))

        try:
            smtp.sendmail('noReply@ILPLabWatch.uni-hamburg.de', to, message)
        except:
            print("E-Mail Versand fehlgeschlagen!")