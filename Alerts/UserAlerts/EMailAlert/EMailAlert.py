from Alerts.AbstractAlert import AbstractAlert
from Ports.AbstractPort import AbstractPort
import datetime, smtplib
from email.mime.text import MIMEText
from email.header import Header

class EMailAlert(AbstractAlert):
    """
    Dieser Alert sendet eine E-Mail Nachricht an die eingesetllten Empfänger, sobald er ausgelöst wird.
    """

    lastCalled = 0
    """der letzte Aufruf des Alerts"""


    def __init__(self, alertID, settings):
        self.lastCalled = datetime.datetime.now() + datetime.timedelta(minutes=-5)
        super().__init__(alertID, settings)

    def throwAlert(self, port, trigger):
        """
        Sendet eine E-Mail an die Empfänger. Eine E-Mail wird erst nach Ablauf der eingestellten Zeit und wenn der Schwellwert zum ersten Mal überschritten wurde versendet.
        """
        td = datetime.timedelta(minutes=-self.getSetting('waitForNextMail'))

        if self.lastCalled < datetime.datetime.now() + td and trigger.isFirstCalled() == True:
            smtp = smtplib.SMTP()
            smtp.connect(host=self.getSetting('SMTPServerAddress'), port=self.getSetting('SMTPServerPort'))
            if self.getSetting('SMTPUsername') != "":
                smtp.login(user=self.getSetting('SMTPUsername'), password=self.getSetting('SMTPPassword'))

            for address in self.getSetting('sendTo').split(';'):
                to = address.strip()
                self.sendMail(to, port, smtp)
            self.lastCalled = datetime.datetime.now()
            smtp.quit()

    def getDescription(self):
        return "Ein E-Mail-Alert sendet eine E-Mail an einen oder mehre Empfänger, wenn der Trigger das erste Mal auslöst."

    def sendMail(self, to, port, smtp):
        """
        Sendet eine E-Mail an einen Empfänger.
        
        :param to: die E-Mailadresse des Empfängers.
        :type to: str
        :param port: der Port der betroffen ist.
        :type port: AbstractPort
        :param smtp: die smtp Verbidnung.
        :type smtp: smptlib.SMPT
        """

        content = "Alert vom Port "+port.getName()+" ausgelöst \n Der Wert vom Port betrug: "+port.getStateWithUnit()+" \n Zusätzliche Nachricht: "+self.getSetting('message')+" \n Zeitpunkt: " + datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        message = MIMEText(content.encode('utf-8'), 'plain', 'utf-8')
        message['From'] = 'ILPLabWatch'
        message['To'] = to
        message['Subject'] = Header("ILPLabWatch Alert ausgelöst", 'utf-8')

        try:
            smtp.sendmail('noReply@ILPLabWatch.uni-hamburg.de', to, message.as_string())
            print("E-Mail an: " + to + " gesendet.")
        except:
            print("Senden der E-Mails fehlgeschlagen!")