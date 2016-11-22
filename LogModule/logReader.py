#This File contains a function to read the log data by a date range

import os, datetime

#log Basedir
basedir = "logs/"

#Function to read the Logs. inputName: the Name of the Port. startDate: the start date of the daterange, endDate: the end date of the daterange; the type of the dates is an instance of datetime; returns a list of the logData
def readLog(inputName, startDate, endDate):
    #The lines that contains the information
    output = []
    #all logfiles that the loop should theoretically read
    logFiles = []

    loopTime = startDate
    while loopTime <= endDate:
        logFileDir = basedir + loopTime.strftime("%Y/%m/{}_%Y_%m_%d.dat".format(inputName))
        logFiles.append(logFileDir)
        loopTime = loopTime + datetime.timedelta(days=1)

    for logFile in logFiles:
        path = logFile

        #exception catching
        try:
            #the actual log file
            f = open(path, "r")
            #the logtime of the file
            logFileParts = os.path.basename(path).split("_")
            name = logFileParts[0]
            year = int(logFileParts[1])
            month = int(logFileParts[2])
            day = int(logFileParts[3].split(".")[0])

            #loop through the files and add all lines that are in the current range
            lines =  f.read().splitlines()
            for line in lines:
                data = line.split(" ")
                logTimeFull = datetime.datetime.strptime(data[0], "%H:%M:%S:%f")
                logDateTime = datetime.datetime(year= year, month= month, day= day, hour=logTimeFull.hour, minute=logTimeFull.minute, second=logTimeFull.second, microsecond=logTimeFull.microsecond)
                if logDateTime >= startDate and logDateTime <= endDate:
                    output.append([name, logDateTime.timestamp(), data[1]])

            f.close()
        except FileNotFoundError:
            continue

    return output

#reads the same as readLog but returns a list of printable Strings.
def readLogStr(inputName, startDate, endDate):
    outputLines = []
    logData = readLog(inputName, startDate, endDate)
    for logPoint in logData:
        outputLines.append(logPoint[0] + " " + logPoint[1] + " " + logPoint[2])
    return outputLines
