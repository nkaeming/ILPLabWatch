from bs4 import BeautifulSoup
# the template class can be used to create awesome UI Views.


class template:
    # holds the whole page Information as a bs4 opbject.
    tagBS = None

    # needs the name of the pagegroup. This can be index, editConf, addPort, logDownload...
    # They can be find in the template.html file in the nav.
    def __init__(self, pagegroup):
        template = open("UI/Helper/template.html", "r")
        template = template.read()
        self.tagBS = BeautifulSoup(template, "html.parser")
        self.setActiveNav(pagegroup)

    # sets the active Navbutton to the correct style. Needs the bs4 object and the view that should be active
    def setActiveNav(self, pagegroup):
        for element in self.tagBS.find("ul", {"class": "navbar-nav"}).findAll("li"):
            if element.find("a")["href"] == "/" + pagegroup:
                element["class"] = "active"
            else:
                element["class"] = ""

    # adds a new bootstrap row to the content block and returns it.
    def addRow(self):
        rowTag = self.tagBS.new_tag("div")
        rowTag["class"] = "row"
        self.tagBS.find("div", {"id": "content"}).append(rowTag)
        return rowTag

    # adds the live update script to the template.
    def addUpdateStatusJS(self):
        newTag = self.tagBS.new_tag("script", src="/CDN/updateStatus")
        template.head.append(newTag)

    # returns a h1 element. Heading size is 1, 2, 3... the bigger the number the smaller...
    def getHeading(self, headingSize, title):
        headingTag = self.tagBS.new_tag("h" + str(headingSize))
        headingTag.string = title
        return headingTag

    # returns the final tags prettifyed and as a byte object
    def getPrettifyedByteObject(self):
        return bytes(str(self.tagBS.prettify()), "utf-8")

    # see bootstrap doc for further informations on the grid system. size is 1-12, offset is 0-11
    def getCollumnDiv(self, size, offset=0):
        divTag = self.tagBS.new_tag("div")
        divTag["class"] = "col-md-" + str(size)
        if offset != 0:
            divTag["class"] = divTag["class"] + " col-md-offset-" + str(offset)
        return divTag

    # see bootstrap doku for the icon names
    def getIcon(self, iconName):
        iconTag = self.tagBS.new_tag("span")
        iconTag["class"] = "glyphicon glyphicon-" + iconName
        iconTag["aria-hidden"] = "true"
        return iconTag