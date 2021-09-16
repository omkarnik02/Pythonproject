
from flask import *

import pymysql
db=pymysql.connect(
    host="localhost",
    user="root",
    password="",
    database="college"
)
cursor=db.cursor()
app=Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


class Student():
    @app.route("/studentlogin")
    def studentlogin():
        return render_template('studentlogin.html') 

    @app.route("/authentication", methods=['post'])
    def authentication():
        un=request.form.get('username')
        pw=request.form.get('password')
        cursor.execute("select * from studentinfo where Username=%s and Password=%s",(un,pw) )
        data1=cursor.fetchone()
        if data1!=None:
            cursor.execute("Select * from studentinfo ")
            headers = [i[0] for i in cursor.description]
            print(data1,headers)
            return render_template('studentinfo.html',data1=data1,headers=headers)
        else:
            return render_template('studentlogin.html',error='Invalid Information')
   
class teachers():
    @app.route("/teacherslogin")
    def teacherslogin():
        return render_template('teacherslogin.html')
    
    @app.route("/tauthentication", methods=['post'])
    def tauthentication():
        un=request.form.get('username')
        pw=request.form.get('password')
        cursor.execute("select * from teachersinfo where Username=%s and Password=%s",(un,pw) )
        data1=cursor.fetchone()
        if data1!=None:
            cursor.execute("Select * from teachersinfo ")
            headers = [i[0] for i in cursor.description]
            session['data'] = data1
            session['ClsAssign'] =data1[4]
            return render_template('teachersinfo.html',data1=data1,headers=headers)
        else:
            return render_template('teacherslogin.html',error='Invalid Information')
    

    @app.route("/teachersinfo")
    def teachersinfo():
        data=session.get('data', None)
        cursor.execute("Select * from teachersinfo ")
        headers = [i[0] for i in cursor.description]
        return render_template('teachersinfo.html',data1=data,headers=headers)
       

    @app.route("/newstudent")
    def newstudent():
        return render_template("newstudent.html")
    
    @app.route("/addstudent", methods=["post"])
    def addstudent():
        name= request.form.get('name')
        age= request.form.get('age')
        address= request.form.get('address')
        mobileno= request.form.get('mobileno')
        gender= request.form.get('gender')
        bloodgroup= request.form.get('bloodgroup')
        Class= request.form.get('Class')
        username= request.form.get('username')
        password= request.form.get('password')
        cursor.execute("select Username from studentinfo")
        UN=cursor.fetchall()
        for i in UN:
            if i[0]==username:
                flash ("Username Already Exist")
                return redirect(url_for('newstudent'))
        
        insq="insert into studentinfo(Name,Age,Address,Mobile_No,Gender,Blood_Group,Class,Username,Password)values('{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(name,age,address,mobileno,gender,bloodgroup,Class,username,password)
        cursor.execute(insq)
        db.commit()
        flash ("Student Added Sussesfully")
        return redirect(url_for('newstudent'))

    @app.route("/ViewStudentData")
    def ViewStudentData():
        Cassign=session.get('ClsAssign', None)
        cursor.execute("select * from studentinfo where Class=%s " ,(Cassign))
        data=cursor.fetchall()
        
        cursor.execute("Select * from studentinfo ")
        headers = [i[0] for i in cursor.description]
        return render_template("studentinfotable.html",data=data,headers=headers)


    @app.route("/editstudent", methods=['post'])
    def editstudent():
        Name=request.form.get('edit')
        cursor.execute("select * from studentinfo where Name=%s ",(Name) )
        data1=cursor.fetchone()
        if data1!=None:
            session['Id'] = data1[0]
            cursor.execute("Select * from studentinfo ")
            headers = [i[0] for i in cursor.description]
            return render_template('editstudent.html',data1=data1,headers=headers)
        else:
            flash ("Student not found")
            data=session.get('data', None)
            cursor.execute("Select * from teachersinfo ")
            headers = [i[0] for i in cursor.description]
            return render_template('teachersinfo.html',data1=data,headers=headers)

    @app.route('/update', methods=['post'] )
    def update():
        header=request.form.get('update1')
        data=request.form.get('update2')
        Id=session.get('Id', None)
        cursor.execute("Select * from studentinfo ")
        headers = [i[0] for i in cursor.description]
        if header=="Id":
            flash ("you can not change Id" )
            cursor.execute("select * from studentinfo where Id=%s " ,(Id))
            data=cursor.fetchone()
            return render_template('editstudent.html',data1=data,headers=headers)
        elif header not in headers:
            flash('enter correct header')
            cursor.execute("select * from studentinfo where Id=%s " ,(Id))
            data=cursor.fetchone()
            return render_template('editstudent.html',data1=data,headers=headers)
        else:
            upq = "UPDATE studentinfo SET {}={} WHERE Id={}".format(header,data,Id)
            cursor.execute(upq)
            db.commit()
            cursor.execute("select * from studentinfo where Id=%s " ,(Id))
            data=cursor.fetchone()
            return render_template('editstudent.html',data1=data,headers=headers)
       
        
   
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

if __name__=="__main__":
    app.run(debug=True)