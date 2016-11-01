import UI.Helper.URLStripper as URLHelper
#This class provides the needed fameworks
#TODO: Work on Performance.
class cdnProvider():
    possibleFrameworks = {
        "jquery" : "jquery.js",
        "bootstrapCSS" : "bootstrap.css",
        "bootstrapTheme" : "bootstrapTheme.css",
        "bootstrapJS" : "bootstrap.js",
        "style": "style.css"
    }

    url = ""
    status = 200
    contentType = "text/html"
    file = None

    def __init__(self, URL):
        self.url = URL
        frameworkName = URLHelper.getSubmodule(self.url)
        if frameworkName in self.possibleFrameworks:
            filename = self.possibleFrameworks[frameworkName]
            self.file = open("UI/CDN/files/" + filename, "r")
            self.status = 200
            type = filename.split(".")[1]
            if type == "js":
                self.contentType = "text/javascript"
            elif type == "css":
                self.contentType = "text/css"
        else:
            self.status = 404

    #returns the http status
    def getStatus(self):
        return self.status

    #returns the content type of the retuned byteobject
    def getContentType(self):
        return self.contentType

    #returns the DisplayString of the content as byte object
    def getDisplayString(self):
        return bytes(self.file.read(), "utf-8")