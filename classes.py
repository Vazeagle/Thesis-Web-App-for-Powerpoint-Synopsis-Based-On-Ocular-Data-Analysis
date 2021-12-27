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

class PowerPointObject:
    def __init__(self, xAxisStart, yAxisStart, width, height, ObjectCategory, minTimestamp, maxTimestamp, occurrenceNum, slideNumber):
        self.xAxisStart = xAxisStart
        self.yAxisStart = yAxisStart
        self.width = width
        self.height = height
        self.ObjectCategory = ObjectCategory
        self.slideNumber = slideNumber

        self.minTimestamp = minTimestamp
        self.maxTimestamp = maxTimestamp
        self.occurrenceNum = occurrenceNum

    def focusDuration(self):
        #should use a try catch for the substraction just to be sure.
        duration = self.maxTimestamp - self.minTimestamp
        print("Duration of Focus on element: in ms", duration)
        return duration

    def focusDuration(self):
        #should use a try catch for the substraction just to be sure.
        duration = self.maxTimestamp - self.minTimestamp
        print("Duration of Focus on element: in ms", duration)
        return duration

class TextBox(PowerPointObject):
    def __init__(self, xAxisStart, yAxisStart, width, height, ObjectCategory, minTimestamp, maxTimestamp, occurrenceNum, slideNumber, text, linesWidth, lineSpacer, yStep, fontName, fontSize, marginLeft, marginRight, marginTop, marginBottom):
        super().__init__(xAxisStart, yAxisStart, width, height, ObjectCategory, minTimestamp, maxTimestamp, occurrenceNum, slideNumber)
        self.text = text
        self.linesWidth = linesWidth
        self.lineSpacer = lineSpacer
        self.yStep = yStep
        self.occurrenceNum = occurrenceNum
        self.fontName = fontName
        self.fontSize = fontSize
        self.marginLeft = marginLeft
        self.marginRight = marginRight
        self.marginTop = marginTop
        self.marginBottom = marginBottom
        
    def getValues(self):
        print("\n")
        print("Values of TextBox:")
        print("TextBoxXstart(removedMargin): ", self.xAxisStart)
        print("TextBoxYstart(removedMargin): ", self.yAxisStart)
        print("TextBoxWidth(removedMargin): ", self.width)
        print("TextBoxHeight(removedMargin): ", self.height)
        print("ParText: ", self.text)
        print("OccurrenceNum", self.occurrenceNum)
        print("EachLineWidth: ", self.linesWidth)
        print("LineSpacer: ", self.lineSpacer)
        print("LineSizeY: ", self.yStep)
        print("FontName: ", self.fontName)
        print("FontSize: ", self.fontSize)
        print("MarginLeft: ", self.marginLeft)
        print("MarginRight: ", self.marginRight)
        print("MarginTop: ", self.marginTop)
        print("MarginBot: ", self.marginBottom)
        print("\n")


class Image(PowerPointObject):
    def __init__(self, xAxisStart, yAxisStart, width, height, ObjectCategory, minTimestamp, maxTimestamp, occurrenceNum, slideNumber, image):
        super().__init__(xAxisStart, yAxisStart, width, height, ObjectCategory, minTimestamp, maxTimestamp, occurrenceNum, slideNumber)
        self.image = image

#class TextBoxWithImage(TextBox, Image):
#    def __init__(textXaxisStart, textYaxisStart, textwidth, textheight, text, fontName, fontSize, marginLeft, marginRight, marginTop, marginBottom, imageXaxisStart, imageYaxisStart, imagewidth, imageheight, image, ObjectCategory, slideNumber):
#??????
#MHPWS INHERITANCE APLA APO PowerPointObject?