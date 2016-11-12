from bs4 import BeautifulSoup
#this file defines some functions for the main layout

#retuns the main template as a bs4 object
def getTemplate():
    template = open("UI/Helper/template.html", "r")
    template = template.read()
    return BeautifulSoup(template, "html.parser")

#sets the active Navbutton to the correct style. Needs the bs4 object and the view taht should be active
def setActiveNav(template, view):
    for element in template.find("ul", {"class": "navbar-nav"}).findAll("li"):
        if element.find("a")["href"] == "/" + view:
            element["class"] = "active"
        else:
            element["class"] = ""

#adds the live update script to the template.
def addUpdateStatusJS(template):
    newTag = template.new_tag("script", src="/CDN/updateStatus")
    template.body.append(newTag)

#sets the heading on a page.
def setHeading(template, heading):
    newTag = template.new_tag("h1")
    newTag.string = heading
    addContentTag(template, newTag)

#adds a Tag to the content div
def addContentTag(template, tag):
    template.find("div", {"id": "content"}).append(tag)