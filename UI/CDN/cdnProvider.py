import UI.Helper.URLStripper as URLHelper
#This class provides the needed fameworks
class cdnProvider():
    possibleFrameworks = {
        "jquery" : "jquery.js",
        "bootstrapCSS" : "bootstrap.css",
        "bootstrapTheme" : "bootstrapTheme.css",
        "bootstrapJS" : "bootstrap.js"
    }

    #returns the DisplayString of the content as byte object
    def getDisplayString(self, URL):
        frameworkName = URLHelper.getSubmodule(URL)
        filename = self.possibleFrameworks[frameworkName]
        file = open("UI/CDN/files/" + filename, "r")
        return bytes(file.read(), "utf-8")