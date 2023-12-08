from flask import Flask,flash,redirect,url_for,request,render_template,jsonify
import mysql.connector
from otp import genotp
from stoken import secret_key
from cmail import sendmail
app=Flask(__name__)
app.secret_key=secret_key
mydb=mysql.connector.connect(host='localhost',user='root',password='anusha@1999',db='spm')
@app.route('/')
def home():
    return render_template('title.html')
@app.route('/registration',methods=['GET','POST'])
def registration():
    if request.method=='POST':
        user=str(request.form['username'])
        password=int(request.form['password'])
        email=request.form['email']
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select username,email from register')
        data=cursor.fetchall()
        print(data)
        print(user,email)
        try:
            if (user,email) in data:
                print('hi')
                raise mysql.connector.IntegrityError
        except mysql.connector.IntegrityError:
            flash('The username is already registred')
            return redirect(url_for('registration'))
        else:
            otp=genotp()
            to=email
            subject='The confirmation otp is sent to your mail'
            body=f'The otp is {otp}'
            sendmail(to,subject,body)
            flash('The confirmation otp is sent to this mail')
            return render_template('otp.html',otp=otp,user=user,password=password,email=email)
    else:
        return render_template('registration.html')
@app.route('/otp/<otp>/<user>/<password>/<email>',methods=['GET','POST'])
def otp(otp,user,password,email):
    if request.method=='POST':
        uotp=request.form['otp']
        if uotp==otp:
            cursor=mydb.cursor(buffered=True)
            cursor.execute('insert into register values(%s,%s,%s)',[user,password,email])
            mydb.commit()
            cursor.close()
            flash('The user is registred successfully')
            return redirect(url_for('login'))
        else:
            flash('The give otp is wrong')
            return render_template('otp.html',otp=otp,user=user,password=password,email=email)
    else:
        return render_template('otp.html')

@app.route('/login',methods=['GET','POST'])
def login():
    return render_template('login.html')
@app.route('/addnotes',methods=['GET','POST'])
def addnotes():
    return render_template('addnotes.html')
@app.route('/viewnotes',methods=['GET','POST'])
def viewnotes():
    return render_template('viewnotes.html')
app.run(debug=True,use_reloader=True)




























