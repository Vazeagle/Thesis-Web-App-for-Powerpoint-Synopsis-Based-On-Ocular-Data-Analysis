#from flask import Flask
#
#app = Flask(__name__)
#
#@app.route("/")
#def hello_world():
#    return "<p>Hello, World!</p>"
#
#if __name__ == "__main__":
#    from waitress import serve
#    serve(app, host="0.0.0.0", port=8080)
#
#    #pip install waitresss
#    #pip install flask
#    #check this for waitress
#    #http://localhost:8080/
#    #https://stackoverflow.com/questions/51025893/flask-at-first-run-do-not-use-the-development-server-in-a-production-environmen
#

from flask import Flask,render_template, request
from flask_mysqldb import MySQL
import subprocess

app = Flask(__name__, template_folder='templates')
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask'
 
mysql = MySQL(app)
 
@app.route('/')
def welcome():
    if request.method == 'GET':
        Newprocess = subprocess.Popen("eye_tracking.py", creationflags = subprocess.CREATE_NEW_CONSOLE)
        processID = Newprocess.pid
        #x=os.getcwd()
        return render_template("/templates\slides\slide_tests/slide0.html") #redirect to main page

@app.route('/<variable>')
def slides(variable):
    #fix the location of the slide change!!!!!!!!
    #if request.method == 'POST':
    #    return render_template('slide0.html')
    #else:
    variable="slides/"+variable
    return render_template(variable)
 
@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'GET':
        return "Login via the login Form"
     
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        cursor = mysql.connection.cursor()
        cursor.execute(''' INSERT INTO options VALUES(%s,%s)''',(name,age))
        mysql.connection.commit()
        cursor.close()
        return f"Done!!"
 
app.run(host='localhost', port=8080)