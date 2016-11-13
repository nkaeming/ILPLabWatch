import UI.Helper.URLStripper as URLHelper
import os
#This class provides the needed fameworks
#TODO: Create a caching mechanism
class cdnProvider():
    url = ""
    status = 200

    def __init__(self, URL):
        self.url = URL
        itemName = URLHelper.getSubmodule(self.url)
        availableItems = []
        for item in os.listdir("UI/CDN/files"):
            availableItems.append(str(item))

        if itemName in availableItems:
            self.file = open("UI/CDN/files/" + itemName, "rb")
            self.status = 200
        else:
            self.status = 404

    #returns the http status
    def getStatus(self):
        return self.status

    #returns the content type of the retuned byteobject
    def getContentType(self):
        return ""

    #returns the DisplayString of the content as byte object
    def getDisplayString(self):
        if self.status == 200:
            return self.file.read()