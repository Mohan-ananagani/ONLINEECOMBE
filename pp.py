from flask import Flask,flash,redirect,url_for,request,render_template,jsonify
import mysql.connector
from otp import genotp
from stoken secret_key
app=Flask(__name__)
app.secret_key=secret_key
mydb=mysql.connector.connect(host='localhost',user='root',password='anusha@1999',db='spm')
@app.route('/')
def home():
    return render_template('title.html')
@app.route('/registration',methods=['GET','POST'])
def registration():
    if request.method=='POST'
    user = request.form['username']
    password= request.form['password']
    email = request.form['email']
    cursor=mydb.cursor(buffered=True)
    try:
        cursor.execute('insert into register values(%s,%s,%s)',[user,password,email])
    except mysql.connector.IntegrityError:
        return 'The username is already Registred'
    else:
        mydb.commit()
        cursor.close()
        flash('good')
        return redirect(url_for('login'))
    '''otp=genotp()
'''
    else:
        return render_template('registration.html')
@app.route('/registration',methods=['GET','POST'])      



