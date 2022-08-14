import pymysql
from flask import Flask,render_template, request, redirect, url_for,session
import os
db_connection=None
db_cursor=None

app = Flask(__name__)
app.secret_key = os.urandom(24)



def db_connet():
    global db_connection,db_cursor
    try:
            db_connection = pymysql.connect(host="localhost",user="root",passwd="",database="employee_db",port=3306)
            print("Connected")
            db_cursor=db_connection.cursor()
            return True
    except:
        print("some error occure, cant connect to database")
        return False

def db_disconnect():
    global db_connection,db_cursor
    db_connection.close()
    db_cursor.close()


#function to fetch data from database
def getAllEmployee():
    isConnected = db_connet()
    if(isConnected):
        print("yes connected")
        getQuery = "select * from employee_info;"  #writting query
        db_cursor.execute(getQuery)           #executing query
        allData = db_cursor.fetchall()        #fetching data from query
        #print(allData)
        db_disconnect()
        return allData




@app.route("/")
def login():
    # return "hello python"
   # allData = getAllStudents()
    return render_template("login.html")

@app.route("/register")
def register():
    # return "hello python"
    # allData = getAllStudents()
    return render_template("register.html")


@app.route("/login_validation", methods = ['GET' , 'POST'])
def login_validation():
    if request.method == "POST":
        data = request.form
        name = data["name"]
        password = data["password"]
        isConnected = db_connet()
        if(isConnected):
            q = "select * from users where user_name = %s and password = %s;"  #writting query
            db_cursor.execute(q,(name,password)) #executing query
            users = db_cursor.fetchall() 
            
            db_disconnect()
    if len(users)>0:
         session['user_id']=users[0][0]
         return redirect(url_for("index"))
    else:
         return redirect(url_for("login"))


@app.route("/add_user", methods=["POST" , "GET"])
def add_user():
     if request.method == "POST":
        data = request.form
        name = data["uname"]
        email = data["uemail"]
        password = data["upassword"]
        isConnected = db_connet()
        if(isConnected):
            q = "insert into users(user_name, email,password) values (%s,%s,%s);"  #writting query
            db_cursor.execute(q,(name,email,password)) #executing query
            db_connection.commit()
            query = "select * from users where user_name = %s and password = %s;"  #writting query
            db_cursor.execute(query,(name,password)) #executing query
            myusers = db_cursor.fetchall() 
            db_disconnect()
            session['user_id'] = myusers[0][0]
            return redirect(url_for("login"))

   


@app.route("/index")
def index():
    # return "hello python"
    allData = getAllEmployee()
    if 'user_id' in session:
         return render_template("index.html",data=allData)
    else:
        return render_template("login.html")     



@app.route("/add", methods = ['GET', 'POST'])
def addStudent():
    
    if request.method == "POST":
        data = request.form
        
        fname = data["fname"]
        
        age = data["age"]
        gender = data["gender"]
        contact = data["contact"]
        email = data["email"]
        address = data["address"]
        job = data["job"]
        hire_date = data["hire_date"]
        department_id = data["department_id"]
        salary = data["salary"]
        isConnected = db_connet()
        if(isConnected):
            insertQuery = "insert into employee_info(f_name,age,gender,contact_no,email,address,job,hire_date,department_id,salary) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"  #writting query
            db_cursor.execute(insertQuery,(fname,age,gender,contact,email,address,job,hire_date,department_id,salary)) #executing query
            db_connection.commit()
            print("Data inserted")
            db_disconnect()
            return redirect(url_for("index"))
    return render_template("add.html")

@app.route('/update/<int:id>', methods = ['GET', 'POST'])
def update(id):
    isConnected = db_connet()
    if(isConnected):
        print("yes connected")
        getQuery = "select * from employee_info where id = %s;"  #writting query
        db_cursor.execute(getQuery,(id))           #executing query
        allData = db_cursor.fetchall()        #fetching data from query
        #print(allData)
        db_disconnect()
        #return allData
    if request.method == "POST":
        data = request.form
        fname = data["fname"]
        
        age = data["age"]
        gender = data["gender"]
        contact = data["contact"]
        email = data["email"]
        address = data["address"]
        job = data["job"]
        hire_date = data["hire_date"]
        department_id = data["department_id"]
        salary = data["salary"]
        isConnected = db_connet()
        if(isConnected):
            updateQuery = "update employee_info set f_name = %s, age = %s, gender = %s, contact_no = %s, email = %s, address = %s, job = %s , hire_date = %s,department_id = %s, salary = %s where id = %s;"  #writting query
            db_cursor.execute(updateQuery,(fname,age,gender,contact,email,address,job,hire_date,department_id,salary,id)) #executing query
            db_connection.commit()
            print("Data updated!!")
            db_disconnect()
            return redirect(url_for("index"))   
    return render_template("update.html", data = allData)
        


   
@app.route("/delete/<int:id>", methods = ['GET', 'POST'])
def delete(id):
    isConnected = db_connet()
    if(isConnected):
            q="delete from employee_info where id=%s"
            db_cursor.execute(q,id)
            db_connection.commit()
            print("Data Deleted!!")
            db_disconnect()
            return redirect(url_for("index"))




@app.route("/logout")
def logout():
    session.pop('user_id')
    return redirect(url_for("login"))


if __name__=="__main__":
    app.run(debug=True)


