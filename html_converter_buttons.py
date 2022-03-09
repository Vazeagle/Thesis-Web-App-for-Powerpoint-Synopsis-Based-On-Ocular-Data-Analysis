#from _typeshed import FileDescriptorLike
from pptx import Presentation
from pptx.util import Cm, Pt
from pptx.dml.color import RGBColor

import aspose.slides as asp_slides
import bs4

import os, shutil
#import glob # for filename opening

def html_slides_creator(powerpointFile, fileName):
    cwd = os.getcwd()
    print("Sheeesh CWD: ",cwd)
    prsDir = cwd+'/tempPowerpointSlides/'

    prs = Presentation(powerpointFile)
    #slide index starts from 0
    slide_counter = 0
    slides_sum = len(prs.slides)
    tempNames=[]
    ##xml_slides.remove(slides[3])

    while slide_counter < slides_sum:
        prs = Presentation(powerpointFile)
        xml_slides = prs.slides._sldIdLst
        slides = list((xml_slides))
        
        for i in range(slides_sum-1,slide_counter,-1):
            xml_slides.remove(slides[i])

        for i in range(0,slide_counter,1):
            xml_slides.remove(slides[i])
        prs.save(prsDir+fileName+"_"+ str(slide_counter) +'.pptx')
        slide_counter+=1
        tempNames.append(fileName+"_"+ str(slide_counter-1) +'.pptx')
        print("tempNames: ",tempNames)


    # Instantiate a Presentation object that represents a PPT file
    #Presentations slides dir
    pptxFileCounter = len(tempNames)-1
    #for file in os.listdir(prsDir):
        #if file.endswith(".pptx"):
            #pptxFileCounter += 1
    #pptxFileCounter=pptxFileCounter-1
    #ADD AN IF ELSE IF NO PPTX FILES EXIST!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


    #for file in os.listdir(prsDir):
        #if file.endswith(".pptx"):
    try:
        for file in tempNames:  #tempNames has the .pptx extension with it
            print("FILE: ", file)
            if (os.path.isfile(prsDir+file)):
                presentation = asp_slides.Presentation(prsDir+file) 

                filename=file.rsplit('.', 1)[0]#remove the .pptx extension of the file for the correct filename
                print("CORECT FILENAME: ", filename)
                # is it this filename== fileName ????????????
                # Save the presentation as HTML

                saveHTML=cwd+"/templates/slides/"+fileName+"/"+filename+".html"
                #saveHTML=cwd+"/htmlSlides/"+fileName+".html"
                path=cwd+"/templates/slides/"+fileName+"/"

                #if file not exists create it!
                if not os.path.exists(path):
                    os.mkdir(path)
                    print("Directory " , path ,  " Created ")
                else:    
                    print("Directory " , path ,  " already exists")

                presentation.save(saveHTML,  asp_slides.export.SaveFormat.HTML)

                # load the file
                with open(saveHTML,"r",encoding="cp437", errors='ignore') as htmlFile: #or utf-8 with html5lib and no delete empty par but delete text of body
                    txt = htmlFile.read()
                    soup = bs4.BeautifulSoup(txt, "lxml")
                    watermark = soup.find('text',{'x':'388.125','y':'229.78125'})   #remove watermark by making it invisible IF we want we can actually delete it
                    watermark['fill-opacity'] = '0.0'
                    scale = soup.find('svg')

                    #This resolution will scale for every user that tries load the slide based on the screen resolution that the browser is currently open
                    scale['width']="1920"   #standard resolution for most pc's monitors
                    scale['height']="1080"
                    scale['id']="svg_scale"

                    script_tag = soup.new_tag("script")
                    script_tag["src"]="{{url_for('static', filename='js/slideRescale.js')}}"

                    par = soup.find('p')
                    par.decompose() #delete empty par base on lxml encoding!
                    trash = soup.find('&#xFEFF; ')
                    body = soup.body #delete margin to have correct resolution!
                    body.append(soup.new_tag('style', type='text/css'))
                    body.style.append('body {margin:0;padding:0}')
                    body["onload"]="rescale();" #rescale js function according to the resolution of the user!
                    body.insert(1,script_tag)#add script location before body of html! 



                    svg_canvas_group = soup.find('g',{'pointer-events':'painted'})
                    #resize RECT AND VIEW BOX OF SVG to correct resolution the rect to have correct button placement
                    #CANT MAKE IT WORK SO USE THE SCALE 960X540 TO PUT THE BUTTONS CORRECT
                    #to fix it chenge view bow to current trsolution and also change scale to scale(2,2)
                    #change rect also to screen resolution!
                    #rect = soup.find('rect',{'fill':'#FFFFFF'})
                    #rect["width"] = "1920" 
                    #rect["height"] = "1080"
                    #rect.decompose() #delete empty par

                    svg_canvas_group.append(soup.new_tag('foreignObject'))
                    foreignObject = soup.foreignObject
                    foreignObject["x"]="800"
                    foreignObject["y"]="520"
                    foreignObject["width"]="150"
                    foreignObject["height"]="25"

                    #new_div = soup.new_tag('div')
                    #new_div["xmlns"]="http://www.w3.org/1999/xhtml"
                    #new_div.string = 'THIS IS A TEST TO CHECK HOW IT WORKS'
                    #foreignObject.append(new_div)

                    #Go to next slide
                    #get current slide number
                    print("fileName: ",fileName+"_")
                    curSlide = int(filename.replace(fileName+"_",""))
                    print("curSlide:",curSlide)
                    if curSlide == pptxFileCounter: #if its the last slide return to start
                        prevSlide = curSlide-1
                        nextLoc = fileName+"_" + "0" + ".html" 
                        prevLoc = fileName+"_" + str(prevSlide) + ".html"
                    elif curSlide==0:#if its the first slide no back stay the same
                        nextSlide = curSlide+1
                        nextLoc = fileName+"_" + str(nextSlide) + ".html"
                        prevLoc = fileName+"_" + "0" + ".html"
                    else:
                        nextSlide = curSlide+1
                        prevSlide = curSlide-1
                        nextLoc = fileName+"_" + str(nextSlide) + ".html"
                        prevLoc = fileName+"_" + str(prevSlide) + ".html"

                    btnExitSlide=soup.new_tag('a',role='button')
                    btnExitSlide["href"]="/synopsis/canceled/cancel"
                    btnExitSlide.append(soup.new_tag('style', type='text/css'))
                    exit_img = soup.new_tag('img', src="{{ url_for('static', filename='exit.png') }}", width="20", height="20")
                    btnExitSlide.append(exit_img)
                    foreignObject.append(btnExitSlide)

                    if curSlide != 0: #IF ITS NOT THE FIRST SLIDE
                        btnPrevSlide=soup.new_tag('a', role='button')
                        btnPrevSlide["href"]="/slides/"+fileName+"/"+ prevLoc+"/bck"
                        btnPrevSlide.append(soup.new_tag('style', type='text/css'))
                        btnPrevSlide.style.append('a {margin:2;}')# if i leave it as button it will interact with all button named elements if i dont want htat i should change the tag name above at 109 and here
                        prev_img = soup.new_tag('img', src="{{ url_for('static', filename='prev.png') }}", width="20", height="20")
                        btnPrevSlide.append(prev_img)
                        foreignObject.append(btnPrevSlide)

                    if curSlide != pptxFileCounter: #IF ITS NOT THE LAST SLIDE
                        btnNextSlide=soup.new_tag('a',role='button')
                        btnNextSlide["href"]="/slides/"+fileName+"/"+ nextLoc+"/fwd"
                        btnNextSlide.append(soup.new_tag('style', type='text/css'))
                        next_img = soup.new_tag('img', src="{{ url_for('static', filename='next.png') }}", width="20", height="20")
                        btnNextSlide.append(next_img)
                        #btnNextSlide.style.append('nextSlideButton {background-color:#0033cc;}')
                        foreignObject.append(btnNextSlide)

                    if curSlide == pptxFileCounter: #if its the last slide add the start synopsis button!
                        btnDoneSlide=soup.new_tag('a',role='button')
                        btnDoneSlide["href"]="/synopsis/"+fileName+"_"+str(curSlide)+"/start"
                        btnDoneSlide.append(soup.new_tag('style', type='text/css'))
                        check_img = soup.new_tag('img', src="{{ url_for('static', filename='check.png') }}", width="20", height="20")
                        btnDoneSlide.append(check_img)
                        foreignObject.append(btnDoneSlide)

                    #SOS TO BE 100% CORRECT I SHOULD SET MANUALLY WHERE THE BUTTONS ARE INSIDE THE FOREIGNOBJECT OF TH "g" tag in the "svg"

                    ##body.append(soup.new_tag('button',type='button'))
                    #button = soup.find("button")
                    #button.append(soup.new_tag('style', type='text/css'))
                    #button.style.append('button {background-color:#0033cc;}')#border:.5px solid crimson;border-radius:10px;color:#fff;padding:8px;height:20px;width:50px;}')

                    sldTitle = soup.findAll('div',{'class':'slideTitle'})
                    for title in sldTitle:
                        title.decompose() #remove slide the extra title div


                with open(saveHTML,"w",encoding="cp437", errors='ignore') as htmlFile:
                    htmlFile.write(str(soup))
    except Exception as e:
        #Delete files from tempSlides Folder if an error occurs!

        for temp_pptxSlide in tempNames:
            file_path = os.path.join(prsDir, temp_pptxSlide)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
        print("An error ocurred during the upload of "+filename)
        print(e)
        return fileName+"_"+".pptx"
    else:
        #Delete files from tempSlides Folder if no exception happened

        for temp_pptxSlide in tempNames:
            file_path = os.path.join(prsDir, temp_pptxSlide)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
        return None

#
#x = range(3,0,-1)
#for n in x:
#    print("sheesh:",n)
#    xml_slides.remove(slides[n])
#x = range(0,0,1)
#for n in x:
#    print("sheesh:2",n)
#    xml_slides.remove(slides[n])
#prs.save('slide'+ str(0) +'.pptx')
#slides = list(copy.copy(xml_slides))
#x = range(3,1,-1)
#for n in x:
#    print("sheesh:",n)
#    xml_slides.remove(slides[n])
#    print("len:",len(xml_slides))
#x = range(0,1,1)
#for n in x:
#    print("sheesh:2",n)
#    xml_slides.remove(slides[n])
#    print("len:",len(xml_slides))
#prs.save('slide'+ str(1) +'.pptx')