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


def readLog(port, start, end):
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
    print(logFiles)
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
                    output.append([name, logDateTime.timestamp(), data[1]])

            f.close()
        except FileNotFoundError:
            continue

    return output


# archiviert die Logs von einem Port.
def archivLog(port):
    # TODO: implement
    pass
