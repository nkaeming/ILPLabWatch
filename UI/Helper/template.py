from bs4 import BeautifulSoup
# the template class can be used to create awesome UI Views.


class template:
    # holds the whole page Information as a bs4 opbject.
    tagBS = None

    # needs the name of the pagegroup. This can be index, editConf, addPort, logDownload...
    # They can be find in the template.html file in the nav. title is the title of the page.
    def __init__(self, pagegroup, title):
        template = open("UI/Helper/template.html", "r")
        template = template.read()
        self.tagBS = BeautifulSoup(template, "html.parser")
        self.setActiveNav(pagegroup)
        self.tagBS.find("div", {"id": "content"}).append(self.getHeading(1, title))

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

    # generates a panel page object (types are primary, warning, error, success, info)
    def getPanel(self, body, header="", footer="", type="primary"):
        panelDivTag = self.tagBS.new_tag("div")
        panelDivTag["class"] = "panel panel-" + type
        # adding the header if necessary
        if header != "":
            headerDiv = self.tagBS.new_tag("div")
            headerDiv["class"] = "panel-heading"
            headerDiv.string = header
            panelDivTag.append(headerDiv)
        # adding the body
        bodyDiv = self.tagBS.new_tag("div")
        bodyDiv["class"] = "panel-body"
        bodyDiv.string = body
        panelDivTag.append(bodyDiv)
        # adding the footer if necessary
        if footer != "":
            footerDiv = self.tagBS.new_tag("div")
            footerDiv["class"] = "panel-footer"
            footerDiv.string = footer
            panelDivTag.append(footerDiv)
        return panelDivTag

    # returns a buttonTag
    def getButton(self, type="submit", style="primary", icon="ok", lable=""):
        buttonTag = self.tagBS.new_tag("button")
        buttonTag["type"] = type
        buttonTag["class"] = "btn btn-" + style
        # add icon if necessary
        if icon != "":
            buttonTag.append(self.getIcon(icon))
        buttonTag.append(lable)
        return buttonTag

    # returns a form tag. action is the URL to direct after submitting
    def getForm(self, action):
        return self.tagBS.new_tag("form", method="GET", action=action)

    # get multiple radio select. radios is a dict with informations {"Name": {"value": X, "lable": X, "disabled"=True/False,"description": X(optional)}} name is the parameter name for the form
    def getMultipleRadioSelect(self, radios, name):
        formGroup = self.tagBS.new_tag("div")
        formGroup["class"] = "form-group"

        for key, value in radios.items():
            # generate formal html code for each element
            outDiv = self.tagBS.new_tag("div")
            outDiv["class"] = "radio"

            lableTag = self.tagBS.new_tag("lable")
            outDiv.append(lableTag)

            # generate the inputTag
            inputTag = self.tagBS.new_tag("input", type="radio", id="radio-" + key, value=value["value"])
            inputTag["name"] = name
            if value["disabled"] == True:
                inputTag["disabled"] = "disabled"

            lableTag.append(inputTag)
            lableTag.append(value["lable"])

            if "description" in value:
                tooltip = self.getTooltipIcon(icon="question-sign", placement="right", tooltip=value["description"])
                lableTag.append(tooltip)

            formGroup.append(lableTag)

        return formGroup

    # returns a popoverbutton
    def getPopoverButton(self, style="primary", icon="", lable="", placement="", popoverTitle="", popoverBody=""):
        buttonTag = self.getButton(type="button", style=style, icon=icon, lable=lable)
        buttonTag["data-toggle"] = "popover"
        if placement != "":
            buttonTag["data-placement"] = placement
        if popoverTitle != "":
            buttonTag["title"] = popoverTitle
        buttonTag["data-content"] = popoverBody
        return buttonTag

    # returns a tooltip icon.
    def getTooltipIcon(self, icon="question-sign", tooltip="", placement=""):
        tooltipTag = self.getIcon(icon)
        tooltipTag["data-toggle"] = "tooltip"
        tooltipTag["title"] = tooltip
        if placement != "":
            tooltipTag["data-placement"] = placement
        return tooltipTag

    # TODO: implement functions to create text, boolean, number and numberrange Formfields.