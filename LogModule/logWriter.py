import os, time, datetime
#logWriter writes the logfiles. It accepts the port and write it automatically.

#the directory of the logfiles.
logDir = "logs/%Y/%m/{}_%Y_%m_%d.dat"

#writes a log
def writeLog(port):
    data = port.getState()
    name = port.getName()
    filepath = time.strftime(logDir.format(name))
    os.makedirs(os.path.dirname(filepath), 0o0777, True)
    f = open(filepath, "a")
    f.write(datetime.datetime.now().strftime("%H:%M:%S:%f") + " " + str(data) + "\n")
    f.close()
