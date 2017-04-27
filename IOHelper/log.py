import datetime
import os
import time

# das Verzeichnis in dem die Logdateien gespeichert werden sollen. Dieser wird von datetime interpretiert, beachte also die Python-Doku.
baseDir = "logs/%Y/%m/"
fileName = "{}_%Y_%m_%d.dat"


# schreibt den Port in eine Logdatei.
def writeLog(port):
    data = port.getState()
    name = port.getName()
    logDir = baseDir + fileName
    filepath = time.strftime(logDir.format(name))
    os.makedirs(os.path.dirname(filepath), 0o0777, True)
    f = open(filepath, "a")
    f.write(datetime.datetime.now().strftime("%H:%M:%S:%f") + " " + str(data) + "\n")
    f.close()


def deleteLog(port):
    """Löscht alle Logdaten eines Ports."""
    year = datetime.datetime.now().year
    runYear = 2017
    portName = port.getName()
    while runYear <= year:
        for runMonth in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']:
            try:
                for fn in os.listdir('logs/' + str(runYear) + '/' + str(runMonth)):
                    if os.path.isfile('logs/' + str(runYear) + '/' + str(runMonth) + '/' + str(fn)):
                        path = 'logs/' + str(runYear) + '/' + str(runMonth) + '/' + str(fn)
                        logFileParts = os.path.basename(path).split("_")
                        name = logFileParts[0]
                        if name == portName:
                            os.remove(path)
            except FileNotFoundError:
                continue
        runYear += 1


def readLog(port, start, end, aboutPoints=0):
    """port ist der Port von dem das Log geladen werde soll. start und end sind datetime objekte."""
    logData = []

    while start <= end:
        datei = (baseDir + fileName).format(port.getName())
        # richtiges Datum einsetzen
        datei = start.strftime(datei)

        # Prüfen ob die Datei existiert
        if os.path.isfile(datei):
            file = open(datei, "r")
            for line in file:
                # Zerteilen der Zeile
                lineContent = line.split(" ")
                dateString = lineContent[0]
                valueString = lineContent[1]

                # Typisierung der Daten
                logTime = datetime.datetime.strptime(dateString, "%H:%M:%S:%f")
                totalDate = datetime.datetime(year=start.year, month=start.month, day=start.day, hour=logTime.hour,
                                              minute=logTime.minute, second=logTime.second,
                                              microsecond=logTime.microsecond)
                value = float(valueString)
                if start <= totalDate and totalDate <= end:
                    logData.append((totalDate, value))
            file.close()

        # Einen Tag dazu zählen, da für jeden Tag eine eigene Datei existiert
        start = start + datetime.timedelta(days=1)

    return logData
