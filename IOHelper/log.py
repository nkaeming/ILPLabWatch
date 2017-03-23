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
                    print(fn)
                    if os.path.isfile('logs/' + str(runYear) + '/' + str(runMonth) + '/' + str(fn)):
                        path = 'logs/' + str(runYear) + '/' + str(runMonth) + '/' + str(fn)
                        logFileParts = os.path.basename(path).split("_")
                        name = logFileParts[0]
                        if name == portName:
                            os.remove(path)
                        print(path)
            except FileNotFoundError:
                continue
        runYear += 1

def readLog(port, start, end, aboutPoints=0):
    """port ist der Port von dem das Log geladen werde soll. start und end sind datetime objekte."""
    # Alle Zeilen, die in dem Zeitraum liegen.
    output = []
    # Alle Logfiles die theoretisch betroffen sind.
    logFiles = []

    loopTime = start
    while loopTime <= end:
        filePath = baseDir + fileName
        logFileDir = loopTime.strftime(filePath.format(port.getName()))
        logFiles.append(logFileDir)
        loopTime = loopTime + datetime.timedelta(days=1)
    for logFile in logFiles:
        path = logFile

        try:
            # the actual log file
            f = open(path, "r")
            # the logtime of the file
            logFileParts = os.path.basename(path).split("_")
            name = logFileParts[0]
            year = int(logFileParts[1])
            month = int(logFileParts[2])
            day = int(logFileParts[3].split(".")[0])

            # loop through the files and add all lines that are in the current range
            lines = f.read().splitlines()
            for line in lines:
                data = line.split(" ")
                logTimeFull = datetime.datetime.strptime(data[0], "%H:%M:%S:%f")
                logDateTime = datetime.datetime(year=year, month=month, day=day, hour=logTimeFull.hour,
                                                minute=logTimeFull.minute, second=logTimeFull.second,
                                                microsecond=logTimeFull.microsecond)
                if logDateTime >= start and logDateTime <= end:
                    output.append((name, logDateTime.timestamp(), data[1]))

            f.close()
        except FileNotFoundError:
            continue

        output = sorted(output, key=lambda dataArray: dataArray[1])

        # TODO: Performance verbessern. Hier werden erst Daten eingelesen und dann gelöscht
        aboutPoints = int(aboutPoints)

        if aboutPoints > 0 and aboutPoints < len(output):
            numberOfDatapoints = len(output)
            intervalLength = int(numberOfDatapoints / aboutPoints)
            if intervalLength > 1:
                newOutput = []
                for i in range(0, numberOfDatapoints):
                    if i % intervalLength == 0:
                        newOutput.append(output[i])
                output = sorted(newOutput, key=lambda dataArray: dataArray[1])
    return output
