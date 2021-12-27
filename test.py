stringTest="This string is line 1.\n\n\nThis is line 2\n         \n\t\t\t\t"

x= stringTest.splitlines()
print(x)
print("type of x:",type(x))
for elem in x:
    if not elem:
        print("null")
    if elem:
        print("not null")
    if elem.isspace():
        print("is space or tab", elem)
        x = list(map(lambda item: item.replace(elem,""), x))
print(x)
for elem in x:
    if not elem:
        print("null")
    else:
        print("not null")


from PIL import Image, ImageDraw, ImageFont
# create an image
out = Image.new("RGB", (150, 100), (255, 255, 255))
# get a font
fnt = ImageFont.truetype("Pillow/Tests/fonts/arial.ttf", 25)
# get a drawing context
d = ImageDraw.Draw(out)
# draw multiline text
d.multiline_text((10, 10), "This is a paragraph test Par5 to test what we see in text when the sentence continues below.", font=fnt, fill=(0, 0, 0))
#out.show()
print("\n\n")

im = Image.new(mode="RGB", size=(1920, 1080))
draw = ImageDraw.Draw(im)

fnt = ImageFont.truetype(font="Tests/fonts/arial.ttf", size=20, encoding="utf-8")

print(draw.multiline_textsize("This is a paragraph test Par to check if the length is represented correctly as it shoulddddddddddddddddd.", font=fnt))
#diff by approx 200pixels frpm emu
#emu diff for full length 1920=1280
#emu mid 613 but is wrong
#emu height is also wrong max is 736.7 in pixels for 1080


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

    def getSlindeNum(self):
        print("Slide number: ", self.slideNumber)
        return self.slideNumber

slides=[0,1]
slide_dict={}
for slide in slides:
    width = 1280
    height = 720
    slideNumber = slide
    slideInfo = Slide(width, height, slide)
    slide_dict['Slide_' + str(slide)] = slideInfo

print(slide_dict)
slide_dict.get('Slide_0').getSlindeNum()
slide_dict.get('Slide_0').getheight()
slide_dict.get('Slide_0').getwidth()

slide_dict.get('Slide_1').getSlindeNum()
slide_dict.get('Slide_1').getheight()
slide_dict.get('Slide_1').getwidth()


from PIL import ImageFont

def get_pil_text_size(text, font_size, font_name):
    font = ImageFont.truetype(font_name, font_size)
    size = font.getsize(text)
    return size
print(get_pil_text_size('This is a paragraph test Par5 to test what we see in text when the sentence continues below.', 24, 'arial.ttf')[1]*1.33)
print(get_pil_text_size(' ', 24, 'arial.ttf')[1]*1.33)
print(get_pil_text_size(' This is itssssssssssssssPsssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss', 24, 'arial.ttf')[1]*1.33)

# importing the module
import json
  
# reading the data from the file
with open('fonts.txt') as f:
    data = f.read()
jsFonts = json.loads(data)
print(jsFonts['Arial'])

print("Check")
realParlength=5
slideResolution=1280
paragraphLines=1

if (realParlength/slideResolution) > int(realParlength/slideResolution):
    paragraphLines = int(realParlength/slideResolution)+1
    print(paragraphLines)
else:
    print(paragraphLines)

test=[]
test.append(123)
print(test)
test=[]
print(test)

x=[0,1,2]
print("len",len(x))



print("TESTING")

space2 = 0
space_list={}
pos = 0 #position of spaces
paragraphsList=["","","sheeesh","test","this","is","a","","kill","me","","",""]
for par in paragraphsList:

    if not par: #If paragraph line is empty and has no text
        space2 +=1
        print("Paragraph line is empty")
        #We need the height of the font in get it with space?
    else:
        print("ParTEXT:",par)
        space_list[pos] = str(space2)+"_" + par
        space2 = 0
        pos+=1
print("")
print(space_list)