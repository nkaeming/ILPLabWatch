from bs4 import BeautifulSoup
#this file defines some functions for the main layout

#retuns the main template as a bs4 object
def getTemplate():
    template = open("UI/Helper/template.html", "r")
    template = template.read()
    return BeautifulSoup(template, "html.parser")