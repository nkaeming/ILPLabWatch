#This File forkes the two main processes for the deamons. One is the webDeaon and the other is the logDeamon
#TODO: Deamons fork
import multiprocessing as mp
from multiprocessing.managers import BaseManager
import Deamons.webDeamon, Deamons.loggerDeamon
from Ports.portService import portService

#This if function is to avoid conflicts n multiprocessing on windows systems
if __name__ == "__main__":
    BaseManager.register('portService', portService)
    manager = BaseManager()
    manager.start()
    ports = manager.portService()
    loggerProcess = mp.Process(target=Deamons.loggerDeamon.loggerDeamon, args=(ports,))
    loggerProcess.start()
    print("Finish Logger init")
    webProcess = mp.Process(target=Deamons.webDeamon.startWebDeamon, args=(ports,))
    webProcess.start()
    webProcess.join()
