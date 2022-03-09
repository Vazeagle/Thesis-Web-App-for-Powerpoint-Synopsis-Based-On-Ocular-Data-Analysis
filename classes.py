class Slide:
    def __init__(self, width, height, slideNumber):
        self.width = width
        self.height = height
        self.slideNumber = slideNumber

    def getwidth(self):
        print("Slide width: ", self.width)
        return self.width

    def getheight(self):
        print("Slide height: ", self.height)
        return self.height

    def getSlideNum(self):
        print("Slide number: ", self.slideNumber)
        return self.slideNumber
    
    def getValues(self):
        print("Width",self.width)
        print("Height",self.height)
        print("SlideNumber",self.slideNumber)
        return {"width":self.width,"height":self.height,"slideNumber":self.slideNumber}

class PowerPointObject:
    def __init__(self, xAxisStart, yAxisStart, width, height, ObjectCategory, slideNumber,objCounter):
        self.xAxisStart = xAxisStart
        self.yAxisStart = yAxisStart
        self.width = width
        self.height = height
        self.ObjectCategory = ObjectCategory
        self.slideNumber = slideNumber
        self.objCounter = objCounter

    def focusDuration(self):
        #-------------------------------------------------------------------------------------------SOS SOS SOS SOS SOS SOS SOS DELETE FROM HERE MAKE AN EXTERNAL FUNCTION FOR DIS!
        #should use a try catch for the substraction just to be sure.
        #duration = self.maxTimestamp - self.minTimestamp
        duration=0
        print("Duration of Focus on element: in ms", duration)
        return duration

    def focusDuration(self):
        #should use a try catch for the substraction just to be sure.
        duration = self.maxTimestamp - self.minTimestamp
        print("Duration of Focus on element: in ms", duration)
        return duration

class TextBox(PowerPointObject):
    def __init__(self, xAxisStart, yAxisStart, width, height, ObjectCategory, slideNumber, objCounter, text, linesWidth, lineSpacer, yStep, fontName, fontSize, marginLeft, marginRight, marginTop, marginBottom, groupID):
        super().__init__(xAxisStart, yAxisStart, width, height, ObjectCategory, slideNumber, objCounter)
        self.text = text
        self.linesWidth = linesWidth
        self.lineSpacer = lineSpacer
        self.yStep = yStep
        self.fontName = fontName
        self.fontSize = fontSize
        self.marginLeft = marginLeft
        self.marginRight = marginRight
        self.marginTop = marginTop
        self.marginBottom = marginBottom
        self.groupID = groupID
        
    def getValues(self):
        print("\n")
        print("Values of TextBox:")
        print("TextBoxXstart(removedMargin): ", self.xAxisStart)
        print("TextBoxYstart(removedMargin): ", self.yAxisStart)
        print("TextBoxWidth(removedMargin): ", self.width)#These are the values of a par  of a textbox!
        print("TextBoxHeight(removedMargin): ", self.height)
        print("ObjectCategory: ", self.ObjectCategory)
        print("slideNumber: ", self.slideNumber)
        print("objCounter: ", self.objCounter)
        print("ParText: ", self.text)
        print("EachLineWidth: ", self.linesWidth)
        print("LineSpacer: ", self.lineSpacer)
        print("LineSizeY: ", self.yStep)
        print("FontName: ", self.fontName)
        print("FontSize: ", self.fontSize)
        print("MarginLeft: ", self.marginLeft)
        print("MarginRight: ", self.marginRight)
        print("MarginTop: ", self.marginTop)
        print("MarginBot: ", self.marginBottom)
        print("GroupID: ", self.groupID)
        print("\n")
        #return these values as dict
        return {"TextBoxXstart(removedMargin)":self.xAxisStart, "TextBoxYstart(removedMargin)":self.yAxisStart, "TextBoxWidth(removedMargin)": self.width, "TextBoxHeight(removedMargin)":self.height,"ObjectCategory":self.ObjectCategory, "slideNumber":self.slideNumber, "objCounter":self.objCounter, "ParText":self.text, "EachLineWidth":self.linesWidth, "LineSpacer":self.lineSpacer, "LineSizeY":self.yStep, "FontName":self.fontName, "FontSize":self.fontSize, "MarginLeft":self.marginLeft, "MarginRight":self.marginRight, "MarginTop":  self.marginTop, "MarginBot": self.marginBottom, "GroupID":self.groupID}

class Image(PowerPointObject):
    def __init__(self, xAxisStart, yAxisStart, width, height, ObjectCategory, slideNumber, objCounter, imageLoc, imageExtensionType, groupID):
        super().__init__(xAxisStart, yAxisStart, width, height, ObjectCategory, slideNumber, objCounter)
        self.imageLoc = imageLoc
        self.imageExtensionType = imageExtensionType
        self.groupID = groupID
    def getValues(self):
        print("\n")
        print("Values of Picture:")
        print("PictureXstart: ", self.xAxisStart)
        print("PictureYstart: ", self.yAxisStart)
        print("PictureWidth: ", self.width)
        print("PictureHeight: ", self.height)
        print("ObjectCategory: ", self.ObjectCategory)
        print("slideNumber: ", self.slideNumber)
        print("objCounter: ", self.objCounter)
        print("imageLoc: ", self.imageLoc)
        print("PictureExtensionType: ", self.imageExtensionType)
        print("GroupID: ", self.groupID)
        print("\n")
        return {"PictureXstart":self.xAxisStart, "PictureYstart":self.yAxisStart, "PictureWidth": self.width, "PictureHeight":self.height,"ObjectCategory":self.ObjectCategory, "slideNumber":self.slideNumber, "objCounter":self.objCounter, "imageLoc":self.imageLoc, "PictureExtensionType":self.imageExtensionType, "GroupID":self.groupID}
        

#class TextBoxWithImage(TextBox, Image):
#    def __init__(textXaxisStart, textYaxisStart, textwidth, textheight, text, fontName, fontSize, marginLeft, marginRight, marginTop, marginBottom, imageXaxisStart, imageYaxisStart, imagewidth, imageheight, image, ObjectCategory, slideNumber):
#??????
#MHPWS INHERITANCE APLA APO PowerPointObject?