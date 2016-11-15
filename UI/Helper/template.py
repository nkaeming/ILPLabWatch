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
        bodyDiv.append(body)
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

    # get strong rendered text
    def getStrongRenderedText(self, text):
        tag = self.tagBS.new_tag("strong")
        tag.string = text
        return tag

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

            lableTag = self.tagBS.new_tag("label")
            outDiv.append(lableTag)

            # generate the inputTag
            inputTag = self.tagBS.new_tag("input", type="radio", id="radio-" + key, value=value["value"])
            inputTag["name"] = name
            if value["disabled"] == True:
                inputTag["disabled"] = "disabled"
                outDiv["class"] = outDiv["class"] + " disabled"

            lableTag.append(inputTag)
            lableTag.append(value["lable"])

            if "description" in value:
                tooltip = self.getTooltipIcon(icon="question-sign", placement="right", tooltip=value["description"])
                lableTag.append(tooltip)

            formGroup.append(outDiv)

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

    # returns a textinput for forms.
    def getTextInput(self, name="", placeholder="", length=35, helpText="", value="", label=""):
        divFormGroup = self.tagBS.new_tag("div")
        divFormGroup["class"] = "form-group"
        labelTag = self.tagBS.new_tag("label")
        labelTag["for"] = "formInput-" + name
        labelTag.append(self.getStrongRenderedText(label))
        inputTag = self.tagBS.new_tag("input", id= "formInput-" + name, placeholder=placeholder, maxlength=length, value = value)
        inputTag["class"] = "form-control"
        inputTag["name"] = name
        inputTag["type"] = "text"

        divFormGroup.append(labelTag)
        divFormGroup.append(inputTag)

        if helpText != "":
            inputTag["aria-describedby"] = "helpBlock-" + name
            divFormGroup.append(self.getInputHelpSpan(helpText, "helpBlock-" + name))

        return divFormGroup

    # returns a checkbox
    def getCheckboxInput(self, name="", value=False, helpText="", label=""):
        divFormGroup = self.tagBS.new_tag("div")
        divFormGroup["class"] = "checkbox"
        labelTag = self.tagBS.new_tag("label")
        inputTag = self.tagBS.new_tag("input", type="checkbox")
        inputTag["name"] = name
        if bool(value) == True:
            inputTag["checked"] = "checked"

        if value == "on":
            inputTag["checked"] = "checked"
        inputTag["id"] = "formInput-" + name
        divFormGroup.append(labelTag)
        labelTag.append(inputTag)
        labelTag.append(label)
        if helpText != "":
            inputTag["aria-describedby"] = "helpBlock-" + name
            divFormGroup.append(self.getInputHelpSpan(helpText, "helpBlock-" + name))

        return divFormGroup

    # returns a numberinput for forms.
    def getNumberInput(self, name="", minValue=0, maxValue=10, step=1, helpText="", value=0, label=""):
        divFormGroup = self.tagBS.new_tag("div")
        divFormGroup["class"] = "form-group"
        labelTag = self.tagBS.new_tag("label")
        labelTag["for"] = "formInput-" + name
        labelTag.append(self.getStrongRenderedText(label))
        inputTag = self.tagBS.new_tag("input", id= "formInput-" + name, value =str(value))
        inputTag["class"] = "form-control"
        inputTag["name"] = name
        inputTag["type"] = "number"
        inputTag["min"] = str(minValue)
        inputTag["max"] = str(maxValue)
        inputTag["step"] = str(step)

        divFormGroup.append(labelTag)
        divFormGroup.append(inputTag)

        if helpText != "":
            inputTag["aria-describedby"] = "helpBlock-" + name
            divFormGroup.append(self.getInputHelpSpan(helpText, "helpBlock-" + name))

        return divFormGroup

    # returns a select input for forms
    def getSelectInput(self, name="", helpText="", values={}, lable="", value=""):
        divFormGroup = self.tagBS.new_tag("div")
        divFormGroup["class"] = "form-group"
        labelTag = self.tagBS.new_tag("label")
        labelTag["for"] = "formInput-" + name
        labelTag.append(self.getStrongRenderedText(lable))
        inputTag = self.tagBS.new_tag("select", id= "formInput-" + name)
        inputTag["class"] = "form-control"
        inputTag["name"] = name

        for displayName in sorted(values.keys(), reverse=False):
            optionTag = self.tagBS.new_tag("option")
            optionTag["value"] = values[displayName]
            if values[displayName] == value:
                optionTag["selected"] = "selected"
            optionTag.string = displayName
            inputTag.append(optionTag)

        divFormGroup.append(labelTag)
        divFormGroup.append(inputTag)

        if helpText != "":
            inputTag["aria-describedby"] = "helpBlock-" + name
            divFormGroup.append(self.getInputHelpSpan(helpText, "helpBlock-" + name))

        return divFormGroup

    # returns a hidden input
    def getHiddenInput(self, name, value):
        inputTag = self.tagBS.new_tag("input", type="hidden", value=value)
        inputTag["name"] = name
        return inputTag

    # returns a help span for form inputs.
    def getInputHelpSpan(self, helpText, id):
        helpTag = self.tagBS.new_tag("span")
        helpTag["class"] = "help-block"
        helpTag["id"] = id
        helpTag.string = helpText
        return helpTag

    # generiert eine Warnmeldung.
    def getAlert(self, text, type="danger"):
        divTag = self.tagBS.new_tag("div")
        divTag["class"] = "alert alert-" + type
        divTag["role"] = "alert"
        divTag.append(text)
        return divTag

    # gibt einen Link als Button zurück.
    def getLinkButton(self, label, href, icon="", type="default"):
        aTag = self.tagBS.new_tag("a", role="button", href=href)
        aTag["class"] = "btn btn-" + type
        if icon != "":
            aTag.append(self.getIcon(icon))
        aTag.append(label)
        return aTag

    # gibt einen HTML Paragraphen zurück.
    def getParagraph(self, text):
        paragraph = self.tagBS.new_tag("p")
        paragraph.append(text)
        return paragraph

    # TODO: implement functions to create numberrange Formfields.