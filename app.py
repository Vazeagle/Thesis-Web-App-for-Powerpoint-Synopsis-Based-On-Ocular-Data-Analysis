from importlib.resources import path
from flask import Flask, flash, render_template, json, request, session, redirect, url_for, abort, send_from_directory
from flask_mysqldb import MySQL
import MySQLdb.cursors
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message
from flask_session import Session
import time
import os
from html_converter_buttons import *
import subprocess
import signal
from startTobiiStream import *
from pptx_element_info import *
from start_eyetracker_recording import *
from multiprocessing import Process, Queue
from dataframe_data_edit import *


mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost' #port is 3306
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'ez-synopsis'
#mysql.init_app(app)
mysql = MySQL(app)

#Flask Mail configurations for gmail(no 2fa in order to work)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'email@gmail.com'
app.config['MAIL_PASSWORD'] = 'passwordformail'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

#Flask Session for user session authentication
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#Flask Upload Folder configuration
app.config['UPLOAD_EXTENSIONS'] = ['.pptx']
app.config['UPLOAD_PATH'] = 'uploads'
#app.config['UPLOAD_FOLDER'] = '/uploads'



@app.route('/')
def main():
    return render_template('index.html')

@app.route('/showSignUp', methods=['POST','GET'])
def showSignUp():
    if request.method == 'POST':
        #These are called based on the id of the html element inside the form!
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']


        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = % s   AND username = % s', (email,username, ))
        data= cursor.fetchone()
        cursor.close()
        if(data):
            return render_template('signup.html',msg='Email already used and username already taken!')
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM user WHERE email = % s ', (email, ))
            data= cursor.fetchone()
            cursor.close()
            if(data):
                return render_template('signup.html',msg='Email already used!')
            else:
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('SELECT * FROM user WHERE username = % s ', (username, ))
                data= cursor.fetchone()
                cursor.close()
                if(data):
                    return render_template('signup.html',msg='Username already taken!')
                else:
                    userID = generate_password_hash(email)
                    password = generate_password_hash(password)
                    passreset = False
                    role = 'user'
                    verified_user = 'no'
                    pptx_settings = 70
                    reg_date = time.strftime('%Y-%m-%d %H:%M:%S')
                    #Insert Data to Database!!!!
                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cursor.execute('INSERT INTO `user`(userID, username, email, password,  passreset, role, verified_user, pptx_settings, reg_date) VALUES (% s, % s, % s, % s, % s, % s, % s, % s, % s)', (userID, username, email, password, passreset, role, verified_user, pptx_settings, reg_date, ))
                    mysql.connection.commit()
                    cursor.close()
                    return render_template('signup.html',msg='You have successfully signed-up!')

    elif request.method == 'GET':
        return render_template('signup.html',msg='')
    #return render_template('slides/slide0.html')

@app.route('/passwordReset')
def passwordReset():
    return render_template('passwordReset.html',msg='')


@app.route('/login', methods=['POST','GET'])
def login():
    if not session.get("name"):
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            cursor.execute('SELECT * FROM user WHERE email = % s ', (email, )) #another way of calling password
            #data = cursor.fetchall()
            data= cursor.fetchone()
            cursor.close()
            if(data):
                print(data['password'])
                if(check_password_hash(data['password'],password)):
                    print("SHEEEEESH")
                    session["name"] = data['userID']    #Insert session ID for current user!
                    if (data['role']== "admin"):  #if its an admin user loggin in
                        return render_template('sideNav.html', msg=" Welcome back " +data['username']+" !", data = ["row1test","row2test","testrow3"])
                    else:   #if its a simple user loggin in
                        return render_template('sideNavUser.html', msg=" Welcome back " +data['username']+" !", data = ["row1test","row2test","testrow3"])
                else:
                    return render_template('login.html',msg='Invalid Email OR Password !')
            else:
                return render_template('login.html',msg='Invalid Email OR Password !')
        elif request.method == 'GET':
            return render_template('login.html',msg='')
        return render_template('login.html',msg='')
    else:   #This will automatically redirect to the sideNav page if user tries to refresh or reload the login page after having logged in
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT username,role FROM user WHERE userID = % s ', (session["name"], )) #another way of calling password
        data= cursor.fetchone()
        cursor.close()
        if (data['role']== "admin"):  #if its an admin user loggin in
            return render_template('sideNav.html', msg=" Welcome back " +data['username']+" !", data = ["row1test","row2test","testrow3"])
        else:   #if its a simple user loggin in
            return render_template('sideNavUser.html', msg=" Welcome back " +data['username']+" !", data = ["row1test","row2test","testrow3"])

@app.route('/logout')
def logout():

    ####delete this call to database later this is only used for testing
    if not session.get("name"):
        return render_template('login.html',msg='')
    else:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT username FROM user WHERE userID = % s ', (session["name"], )) #another way of calling password
        data= cursor.fetchone()
        cursor.close()

        session["name"] = None
        return render_template('login.html',msg = data["username"]+' successfully logged out!')

@app.route('/sideNav')
def showSideNav():
    if not session.get("name"):
        return render_template('login.html',msg='')
    else:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT username,role FROM user WHERE userID = % s ', (session["name"], )) #another way of calling password
        data= cursor.fetchone()
        cursor.close()
        print("data['role']:",data['role'])
        if (data['role']== "admin"):  #if its an admin user loggin in
            return render_template('sideNav.html', msg=" Welcome back " +data['username']+" !", data = ["row1test","row2test","testrow3"])
        else:   #if its a simple user loggin in
            return render_template('sideNavUser.html', msg=" Welcome back " +data['username']+" !", data = ["row1test","row2test","testrow3"])

#
#This upload will overwrite existing files with the same name!
#maybe create a delete function if we have time
#
@app.route('/uploads', methods=['GET', 'POST'])
def upload_file():
    if not session.get("name"):
        return render_template('login.html',msg='')
    else:
        #GET ADMIN-USER INFORMATION
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT username,role FROM user WHERE userID = % s ', (session["name"], )) #another way of calling password
        data= cursor.fetchone()
        cursor.close()
        
        if data['role']=="admin":
                
            if request.method == 'POST':

                # check if the post request has the file part
                upload_file = request.files.getlist('file')
                print("upload_file: ",upload_file)
                if (upload_file[0].filename =='' and len(upload_file)==1):   #this because  if the user selects upload without selecting a file it will return a list with an empty file storage object!
                    return render_template('uploads.html', msg_fail = "No selected file! Please select one or more pptx file/files to upload !", files_fail = [], msg_success = "", files_ok = [])
                else:
                    data_ok=[]
                    data_fail=[]
                    html_fail=[]
                    for file in upload_file:
                        filename = secure_filename(file.filename)
                        print("FLASK FILENAME: ",filename)
                        if filename != '':  #this check is because secure_filename can return an empty filename
                            file_ext = os.path.splitext(filename)[1]
                            file_name = os.path.splitext(filename)[0]
                            print("Sheeeeesh file ext",file_ext)
                            print("Sheeeeesh file NAME",file_name)
                            if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                                data_fail.append(file)
                                return render_template('uploads.html', msg_fail = "The following file upload is unsupported: "+ filename, files_fail = [], msg_success = "", files_ok = [])
                                #abort(400)
                            else:
                                #file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
                                subFile = os.path.join(app.config['UPLOAD_PATH'], file_name)
                                save_path = os.path.join(app.config['UPLOAD_PATH'], file_name , filename)
                                if(os.path.exists(subFile)):
                                    file.save(save_path)
                                else:
                                    os.makedirs(subFile)
                                    file.save(save_path)
                                data_ok.append(file)
                                #htmlSlideCreation! call function!!
                                res = html_slides_creator(save_path, file_name)
                                #*****************************************************&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
                                #*****************************************************&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
                                #*****************************************************&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
                                #*****************************************************&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
                                #*****************************************************&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
                                #Check if file already exists if yes delete the old record and insert later the new one
                                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                                cursor.execute('SELECT powerpoint_name  FROM powerpoint_files WHERE powerpoint_name = % s ', (file_name, ))
                                data_check= cursor.fetchone()
                                cursor.close()
                                print("SHEESH!",data)
                                if(data_check is None): #if data is None
                                    #Insert Data to Database FOR powerpoint_files!!!!
                                    upload_date = time.strftime('%Y-%m-%d %H:%M:%S')
                                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                                    cursor.execute('INSERT INTO powerpoint_files(powerpoint_name, uploader, upload_date, save_location) VALUES (% s, % s, % s, % s)', (file_name, data['username'], upload_date, save_path, ))
                                    mysql.connection.commit()
                                    cursor.close()
                                else: #IF PPTX EXIST IN DATABASE REMOVE IT AND RE-INSERT THE DATA
                                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                                    cursor.execute('DELETE FROM powerpoint_files WHERE powerpoint_name = % s ', (file_name, ))
                                    mysql.connection.commit()
                                    cursor.close()
                                    #RE-INSERT DATA
                                    upload_date = time.strftime('%Y-%m-%d %H:%M:%S')
                                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                                    cursor.execute('INSERT INTO powerpoint_files(powerpoint_name, uploader, upload_date, save_location) VALUES (% s, % s, % s, % s)', (file_name, data['username'], upload_date, save_path, ))
                                    mysql.connection.commit()
                                    cursor.close()
                                pptx_elements = gatherData(save_path, file_name) #pptx_elements is a list that contains two sub list the first one has as elements dictionaries of textbox class and the other dict of picture class
                                print("SLIDES DICTIONARIES LIST: ",pptx_elements[2])
                                #INSERT Picture ELEMENTS TO DB
                                for class_dict in pptx_elements[2]:
                                    #Insert Data to Database!!!!
                                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                                    print("class_dict_pic: ", class_dict)
                                    cursor.execute('INSERT INTO slides(pptx_name, slide_number, slide_width, slide_height) VALUES (% s, % s, % s, % s)', (file_name, class_dict['slideNumber'], class_dict['width'], class_dict['height'], ))
                                    mysql.connection.commit()
                                print("TEXTBOX DICTIONARIES LIST: ",pptx_elements[0])
                                #INSERT TEXT_BOXES ELEMENTS TO DB
                                for class_dict in pptx_elements[0]:
                                    #Insert Data to Database!!!!
                                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                                    print("class_dict_text: ", class_dict)
                                    #cursor.execute('INSERT INTO textbox_elements(pptx_name, slide_number, object_counter, textBoxXstart_no_margin, textBoxYstart_no_margin, textBoxWidth_no_margin, textBoxHeight_no_margin, objectCategory, parText, minTimestamp, maxTimestamp, OccurrenceNum, eachLineWidth) VALUES (% s,% s,% s,% s,% s,% s,% s, % s, % s, % s, % s, % s, % s)', (file_name, class_dict['slideNumber'], class_dict['objCounter'], class_dict['TextBoxXstart(removedMargin)'], class_dict['TextBoxYstart(removedMargin)'], class_dict['TextBoxWidth(removedMargin)'], class_dict['TextBoxHeight(removedMargin)'], class_dict['ObjectCategory'], class_dict['ParText'], class_dict['minTimestamp'], class_dict['maxTimestamp'], class_dict['OccurrenceNum'], class_dict['EachLineWidth'],))
                                    eachLineWidth = ', '.join(list(map(str, class_dict['EachLineWidth'])))# because it returns and array that shows the width of each line width inside a paragraph
                                    #(map(str, class_dict['EachLineWidth'])) converts the float to str in order to join them as a str!
                                    cursor.execute('INSERT INTO textbox_elements(pptx_name, slide_number, object_counter, textBoxXstart_no_margin, textBoxYstart_no_margin, textBoxWidth_no_margin, textBoxHeight_no_margin, objectCategory, parText, eachLineWidth, lineSpacer, lineSizeY, fontName, fontSize, marginLeft, marginRight, marginTop, marginBot, groupID) VALUES (% s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s)', (file_name, class_dict['slideNumber'], class_dict['objCounter'], class_dict['TextBoxXstart(removedMargin)'], class_dict['TextBoxYstart(removedMargin)'], class_dict['TextBoxWidth(removedMargin)'], class_dict['TextBoxHeight(removedMargin)'], class_dict['ObjectCategory'], class_dict['ParText'], eachLineWidth, class_dict['LineSpacer'], class_dict['LineSizeY'], class_dict['FontName'], class_dict['FontSize'], class_dict['MarginLeft'], class_dict['MarginRight'], class_dict['MarginTop'], class_dict['MarginBot'], class_dict['GroupID'], ))
                                    mysql.connection.commit()
                                    cursor.close()
                                print("PICTURES DICTIONARIES LIST: ",pptx_elements[1])
                                #INSERT Picture ELEMENTS TO DB
                                for class_dict in pptx_elements[1]:
                                    #Insert Data to Database!!!!
                                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                                    print("class_dict_pic: ", class_dict)
                                    cursor.execute('INSERT INTO picture_elements(pptx_name, slide_number, object_counter, pictureXstart, pictureYstart, pictureWidth, pictureHeight, objectCategory, imageLoc, pictureExtensionType, groupID) VALUES (% s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s)', (file_name, class_dict['slideNumber'], class_dict['objCounter'], class_dict['PictureXstart'], class_dict['PictureYstart'], class_dict['PictureWidth'], class_dict['PictureHeight'], class_dict['ObjectCategory'], class_dict['imageLoc'], class_dict['PictureExtensionType'], class_dict['GroupID'], ))
                                    mysql.connection.commit()
                                #UPLOAD TO DATABASE WITH ONE INSERT
                                #def get_values_of_dicts_in_list(dict_list):
                                #    result_list=[]
                                #    for dict in dict_list:
                                #        result_list.append(dict.values())
                                #    return result_list
                                #https://softhints.com/insert-multiple-rows-at-once-with-python-and-mysql/
                                #*****************************************************&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
                                #*****************************************************&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
                                #*****************************************************&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
                                #*****************************************************&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
                                #*****************************************************&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
                                #*****************************************************&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
                                if res is not None:#when no failure occurs it returns None, and we don't wont to append the list then because  it will print it in msg_fail
                                    html_fail.append(res)
                    #if html conversion fails!
                    if(html_fail):
                        return render_template('uploads.html', msg_fail = "The following file/files conversion to html has failed, please retry uploading them: ", files_fail = html_fail, msg_success = "The following pptx files were uploaded successfully to the server: ", files_ok = data_ok)
                    else:
                        if(data_fail):   # if data_fail is not empty
                            return render_template('uploads.html', msg_fail = "The following file/files uploading is unsupported: ", files_fail = data_fail, msg_success = "The following file/files were uploaded successfully: ", files_ok = data_ok)
                        else:   #if data_fail empty means all uploads were successfull
                            return render_template('uploads.html', msg_fail = "", files_fail = [], msg_success = "All files were uploaded successfully! ", files_ok = [])
            else:
                return render_template('uploads.html', msg_fail = "", files_fail = [], msg_success = "", files_ok = [])
        else:   #if its an USER show error!!!
           return render_template('uploads.html', msg_fail = "You shouldn't be here. Only Admin can upload!", files_fail = [], msg_success = "", files_ok = [])

@app.route('/files', methods=['GET']) #only get!!!!!!
def get_files():
    if not session.get("name"):
        return render_template('login.html',msg='')
    else:
        if request.method == 'GET':
            #Call uploaded files from db and show them with message jinja2 fro loop!!!
            slidesLoc = os.getcwd()+"/templates/slides/"
            slideNamesList = os.listdir(slidesLoc)
            killedPID = killTobiiStream()
            print("killedPID: ", killedPID)
            return render_template('files.html', files = slideNamesList)

#
#@app.route('/slides')
#def welcome():
#    if request.method == 'GET':
#        #Newprocess = subprocess.Popen("eye_tracking.py", creationflags = subprocess.CREATE_NEW_CONSOLE)
#        #processID = Newprocess.pid
#        #x=os.getcwd()
#        return render_template("slides/slide0.html") #redirect to main page
#
#        
#@app.route('/<variable>')
#def slides(variable):
#    variable="slides/"+variable
#    return render_template(variable)

pid_info=[]
@app.route('/slides/<folder>/<file>/<action>')
def slides(folder,file,action):

    if not session.get("name"):
        return render_template('login.html',msg='')
    else:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT username FROM user WHERE userID = % s ', (session["name"], )) #another way of calling password
        db_user_data= cursor.fetchone()
        cursor.close()

        TobiiStream= startTobiiStream() #will return the current pid
        print("TobiiStream PID:",TobiiStream)

        if (pid_info): #if list is not empty
            for pid in pid_info:
                print("SOS SOS SOS SOS SOS SOS SOS SOS SOS PID: ",pid)
                pid[0].terminate()
                #subprocess.Popen.kill(pid[1]) #This works!!!!
                pid_info.clear()

            #maybe a function that renames the csv based on the slideNumber and then it fixes the data!
            #SOS SOS SOS SOS SOS SOS SOS SOS SOS SOS SOS SOS SOS SOS SOS SOS
            #SOS SOS SOS SOS SOS SOS SOS SOS SOS
            data_list = fix_ocular_data()
            #INSERT TO DATABASE!!!

            #get current slide number
            filename=file.rsplit('.', 1)[0]#remove the .html extension of the file for the correct filename
            correct_filename=filename.rsplit('_', 1)[0] #this is the correct name of the pptx file with out the added "_" that came  from the html slides creation

            #Current Slide Number
            curSlideNum = int(filename.split("_")[-1])
            if action=="fwd":
                slideNumber = curSlideNum-1
            elif action=="bck":
                slideNumber = curSlideNum+1
            else:
                print("ERROR!!!")
                print("INCORRECT URL!! RETURN TO FILES")
                slideNumber="NAN"

            print("FLASK SLIDENUMBER: ",slideNumber)
            #slidesLoc = os.getcwd()+"\\templates\\slides\\"+correct_filename
            username = db_user_data['username']
            #INSERT INTO ocular_data
            for eyeTracking_triplet in data_list:
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('INSERT INTO ocular_data(pptx_name, slide_number, username, coordinateID, Xcoordinates, Υcoordinates, Τimestamp, collection_date) VALUES (% s, % s, % s, % s, % s, % s, % s, % s)', (correct_filename, slideNumber, username, None, eyeTracking_triplet[1], eyeTracking_triplet[2], eyeTracking_triplet[0], time.strftime('%Y-%m-%d %H:%M:%S'), ))
                mysql.connection.commit()
                cursor.close()
            
            #Start again the eyetracking recording!
            res = start_recording_OcularData()
            print("AFTER THE FUNCTION start_recording_OcularData():", res)
            print("ADD PID TO PID_INFO LIST!!!!")
            pid_info.append(res)

        else:
            #First load of first slide start the recording of data
            res = start_recording_OcularData()
            print("AFTER THE FUNCTION start_recording_OcularData():", res)
            print("ADD PID TO PID_INFO LIST!!!!")
            pid_info.append(res)
            #dataframe = fix_ocular_data()


        #time.sleep(10)
        #res[0].communicate(input='0x03')#0x03
        #res[0].send_signal(signal.SIGINT)#0x03
        #os.kill(res[1], signal.CTRL_C_EVENT)
        #
        #subprocess.Popen.kill(res[0]) #This works!!!!---------------------------------------------------------------------------
        #
        #os.kill(res[1], signal.CTRL_BREAK_EVENT)#no work
        #res[0].send_signal(signal.CTRL_C_EVENT)# no work
        #os.kill(res[1], signal.CTRL_C_EVENT)
        #res[0].send_signal(SIGINT)
        #https://stackoverflow.com/questions/7085604/sending-c-to-python-subprocess-objects-on-windows
        #Newprocess = subprocess.Popen("python eye_tracking.py", creationflags = subprocess.CREATE_NEW_CONSOLE)
        #processID = Newprocess.pid
        #print(processID)
        #os.kill.send_signal(signal.SIGINT)
        #os.kill(TobiiStream, signal.SIGTERM)
        #Check if pid exists in termination close this propcess to save ram!
        #open with a new popen the python eye_tracking.py file and then get its PID  to send it later an interrupt signal on page change!
        #or a keyboard interupt or pid interupt
        #after that either save to the DB THE OCULAR DATA EITHER ON A DATAFRAME TO CHECK THE OCCURENCES!
        #form the other file the pptx_run.py
        ##https://stackoverflow.com/questions/13024532/simulate-ctrl-c-keyboard-interrupt-in-python-while-working-in-linux
        #os.system('python eye_tracking.py')# serial running
        #Newprocess = subprocess.Popen("python startTobiiStream.py", creationflags = subprocess.CREATE_NEW_CONSOLE)
        #Record_eye_process = subprocess.Popen("eye_tracking.py", creationflags = subprocess.CREATE_NEW_CONSOLE)
        #processID = Record_eye_process.pid
        #Record_eye_process.send_signal(signal.SIGINT)
        #queue = Queue()
        #Record_eye_process = Process(target=recordOcularData())
        #Record_eye_process.start()
        #print("PID IS: ",Record_eye_process.pid)
        #print("NAME IS: ",Record_eye_process.name)
        #print("IS ALIVE: ",Record_eye_process.is_alive())
        #result = queue.get()
        #print("RESULT!!!!!: ",result)
        #args=(queue, 1)
        #https://docs.python.org/3/library/multiprocessing.html#the-process-class

        #print("Record_eye_process PID: ",processID)
        #time.sleep(5)
        path = "slides/"+folder+"/"+file
        print("PATH variable",path)
        return render_template(path)

#SOS SOS SOS SOS SOS SOS SOS SOS SOS SOS SOS SOS SOSSOS SOS SOS SOS SOS SOS SOS
#Add in the html converter separate folders for each slide and save in there the html slides
#Also modify thehtml slides location by adding /slides/"folder"/slide0.html for each one!
#try this with url_for for flask!
#Also for the href for the page redirrection for the /files it should have something like:
#<li role="presentation"><a href="/slides/slide0.html">Slidess</a></li> maybe with one more folder and the name of the first slide!
#add an alert to go full screen! f11 or actually add it on the scale javascript file taht will do fullscreen for every body!

#*****************************************************&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
#*****************************************************&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
#*****************************************************&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
#*****************************************************&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&



@app.route("/synopsis/<LastSlideName>/<status>", methods=['GET'])
def synopsis(LastSlideName,status):
    if not session.get("name"):
        return render_template('login.html',msg='')
    else:
        if(status=="start"):
            
            #INSERT TO DATABASE THE LAST SLIDE INFORMATION!
            if(pid_info):
                for pid in pid_info:
                    pid[0].terminate()#kill the process!
                    #subprocess.Popen.kill(pid) #This works!!!!
                    print("Current PID KILLED: ",pid)
                    pid_info.remove(pid)

            data_list = fix_ocular_data()
            
            #GET USERNAME
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT username FROM user WHERE userID = % s ', (session["name"], )) #another way of calling password
            db_user_data= cursor.fetchone()
            cursor.close()

            correct_filename=LastSlideName.rsplit('_', 1)[0] #this is the correct name of the pptx file with out the added "_" that came  from the html slides creation
            slideNumber = int(LastSlideName.split("_")[-1])#cause its the last slide !!!!
            print("FLASK SLIDENUMBER: ",slideNumber)
            #slidesLoc = os.getcwd()+"\\templates\\slides\\"+correct_filename
            username = db_user_data['username']
            
            #INSERT INTO ocular_data
            for eyeTracking_triplet in data_list:
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('INSERT INTO ocular_data(pptx_name, slide_number, username, coordinateID, Xcoordinates, Υcoordinates, Τimestamp, collection_date) VALUES (% s, % s, % s, % s, % s, % s, % s, % s)', (correct_filename, slideNumber, username, None, eyeTracking_triplet[1], eyeTracking_triplet[2], eyeTracking_triplet[0], time.strftime('%Y-%m-%d %H:%M:%S'), ))
                mysql.connection.commit()
                cursor.close()


                
            #THIS BLOCK WILL HAVE A USE AS A REDIRECT SINCE WE NEED TO INFORM THE USER THAT THE SYNOPSIS
            #HAS STARTED AND THAT HE WILL HAVE TO WAIT TO GET THE RESULTS!!
            #SO WE CALL AGAIN THE SAME URL BUT WITH running as variable to enter the elif and start there the synopsis while having rendered the user a wait message
            #When the synopsis will finish the user will be redirected to the synopsis files
            message = "Please wait until the synopsis is finished and get automatically redirected to it!"
            print("WEEEEEEEEEEEEEEEEEEEEEEEE!")
            #https://stackoverflow.com/questions/53320037/python-redirect-with-delay
            return render_template('synopsis.html',msg=message), {"Refresh": "1; url=http://127.0.0.1:5002/synopsis/synopsisCreation/running"}#ONE SEC DELAY!
        elif(status=="running"):
            #SOS SOS SOS SOS SOS SOS SOS SOS SOS Start Synopsis here




            #Create Synopsis
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT username FROM user WHERE userID = % s ', (session["name"], )) #another way of calling password
            data= cursor.fetchone()
            cursor.close()
            #CREATE SAVE FOLDER!
            path=cwd+"/synopsis/"+data['username']#we could use the session["name"] which is the userID for anonymity but because of the hash string it might be unreachable by the os beacuse of it's characters so we will use the username!
            #if file not exists create it!
            if not os.path.exists(path):
                os.mkdir(path)
                print("Directory " , path ,  " Created ")
            else:
                print("Directory " , path ,  " already exists")






            print("Hello World ITS ME AGAIN!")
            time.sleep(5)
            print("I WOKE UP!!!!")
            return redirect(url_for('synopsisFiles'))
        
        elif(status=="cancel"):
            if(pid_info):
                for pid in pid_info:
                    pid[0].terminate()
                    #subprocess.Popen.kill(pid) #This works!!!!
                    print("Current PID KILLED because of user cancelation: ",pid)
                    pid_info.remove(pid)

            message = "Synopsis was Canceld by the user! Any data that were gathered will be discarded!"
            return render_template('synopsis.html',msg=message)

        else:

            if(pid_info):
                for pid in pid_info:
                    pid[0].terminate()
                    #subprocess.Popen.kill(pid) #This works!!!!
                    print("Current PID KILLED because of unknown error! ",pid)
                    pid_info.remove(pid)
            message = "Unknown error please retry to create the synopsis!"
            return render_template('synopsis.html',msg=message)








@app.route("/synopsisFiles", methods=['GET'])
def synopsisFiles():
    if not session.get("name"):
        return render_template('login.html',msg='')
    else:
        killedPID = killTobiiStream()
        print("SYNOPSISFILES killedPID: ", killedPID)
        
        #call db with userID and check if user is admin!!!!
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT username,role FROM user WHERE userID = % s ', (session["name"], )) #another way of calling password
        data= cursor.fetchone()
        cursor.close()
        #IF USERID IS NOT THE ONE OF THE ADMIN ONLY MAKE VISIBLE THE ONES FOR EACH USER!
        #ADMIN CAN SEE ALL SYNOPSIS!
        #ADD ELSE FOR ADMIN
        print(data['role'])
        if data['role'] != "admin":
            #Access specific user synopsis only!
            synopsisLoc = os.getcwd()+"\\synopsis\\"+data['username']
            print(synopsisLoc)
            try:
                synopsisSumDict={}
                synopsisNamesList = os.listdir(synopsisLoc)
                empty=False
            except:
                synopsisSumDict={}
                empty=True
            if(empty):
                return render_template('synopsisFiles.html',msg="You have no Synopsis files!", files = synopsisSumDict)
            else:
                for synopsis in synopsisNamesList:
                    print("synopsisFILE: ",synopsis)
                    synopsisSumDict[synopsis]="\\download\\"+data['username']+"\\"+synopsis
                else:
                    return render_template('synopsisFiles.html',msg="", files = synopsisSumDict)
        else:
            synopsisSumDict={}
            synopsisDirLoc = os.getcwd()+"\\synopsis\\"
            subDirsList = os.listdir(synopsisDirLoc)
            for dir in subDirsList:
                subDirLoc = os.getcwd()+"\\synopsis\\"+dir
                subDirsSynopsisList = os.listdir(subDirLoc)
                for synopsis in subDirsSynopsisList:
                    print("synopsisFILE: ",synopsis)
                    synopsisSumDict[synopsis]="\\download\\"+dir+"\\"+synopsis# do i need pptx file extension here? #synopsis must have a unique name!

            return render_template('synopsisFiles.html', files = synopsisSumDict)

@app.route("/download/<dir>/<file_name>", methods=['GET'])
def download(dir, file_name):
    if not session.get("name"):
        return render_template('login.html',msg='')
    else:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT username,role FROM user WHERE userID = % s ', (session["name"], )) #another way of calling password
        data= cursor.fetchone()
        cursor.close()
        if data['role'] != "admin":

            downloadDir=os.getcwd()+"\\synopsis\\"+data["username"] #we used this for security reasons because if a user maliciously change the html dir
            # like form before he could get nay file he wanted from the server!!!!!

            print(downloadDir)
            return send_from_directory(directory = downloadDir, path = file_name, as_attachment=True)

        #Admin can download anything!!!!!
        else:
            downloadDir=os.getcwd()+"\\synopsis\\"+dir
            print(downloadDir)
            return send_from_directory(directory = downloadDir, path = file_name, as_attachment=True)


@app.route("/settings", methods=['GET', 'POST'])
def setttings():
    acceptable_settings=[50,60,70,80,90]
    if not session.get("name"):
        return render_template('login.html',msg='')
    else:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT pptx_settings FROM user WHERE userID = % s ', (session["name"], )) #another way of calling password
        data= cursor.fetchone()
        cursor.close()

        if request.method == 'POST':
            
            #Get form data!!!!!!
            new_settings = int(request.form['settings'])
            if new_settings in acceptable_settings:
                
                #Insert New Settings!!!
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('UPDATE `user` SET pptx_settings = % s WHERE userID = % s ', (new_settings,session["name"], )) #another way of calling password
                mysql.connection.commit()
                cursor.close()

                #Check New Settings Price!!!
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('SELECT pptx_settings FROM user WHERE userID = % s ', (session["name"], )) #another way of calling password
                data= cursor.fetchone()
                cursor.close()

                return render_template('settings.html',msg='Current Percentage Value: '+ str(data['pptx_settings']), error_msg="")

            else:
                return render_template('settings.html',msg='Current Percentage Value: '+ str(data['pptx_settings']), error_msg="Please Choose one of the acceptable prices!")

        elif request.method == 'GET':
            return render_template('settings.html',msg='Current Percentage Value: '+ str(data['pptx_settings']), error_msg="")

#https://stackoverflow.com/questions/66880261/how-to-make-long-text-fit-into-a-text-frame-python-pptx



@app.route("/mail")
def send_email():
  msg = Message('Welcome to Ez-Synopsis. Please Verify your account!', sender =   '@gmail.com', recipients = ['reciever'])
  msg.body = "Welcome"+"username"+", thank you for using  Ez-Synopsis"
  #if we want to send an attachment!
  #with app.open_resource("invoice.pdf") as fp:
  #msg.attach("invoice.pdf", "application/pdf", fp.read())  
  mail.send(msg)
  return "Message sent!"


if __name__ == "__main__":
    app.debug=True
    app.run(host='localhost',port=5002)
    #app.run(host='192.168.1.4',port=5002)
