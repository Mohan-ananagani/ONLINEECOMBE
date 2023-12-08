from flask import Flask,flash,redirect,url_for,request,render_template,jsonify,session
from flask_session import Session
import mysql.connector
from otp import genotp
from stoken import secret_key,token
from itsdangerous import URLSafeTimedSerializer
from key import secret_key,salt
from cmail import sendmail
app=Flask(__name__)
app.secret_key=secret_key
mydb=mysql.connector.connect(host='localhost',user='root',password='Admin',db='spm')
@app.route('/')
def index():
    return render_template('title.html')
@app.route('/registration',methods=['GET','POST'])
def registration():
    if request.method=='POST':
        user=str(request.form['username'])
        password=int(request.form['password'])
        email=request.form['email']
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select count(*) from register where username=%s',[user])
        count=cursor.fetchone()[0]
        print(count)
        cursor.execute('select count(*) from register where email=%s',[email])
        count1=cursor.fetchone()[0]
        print(count1)
        if count==1:
            flash('The username is already registered.')
            return redirect(url_for('registration'))
        elif count1==1:
            flash('The email has already registered.')
            return redirect(url_for('registration'))
        data={'username':user,'password':password,'email':email}
        subject='The onetime link for login application'
        body=f"Follow up the give url for further steps{url_for('confirm',token=token(data),_external=True)}"
        sendmail(to=email,subject=subject,body=body)
        flash('One time link has sent your email pls confirm.')
        return redirect(url_for('login'))
    else:
        return render_template('registration.html')
@app.route('/confirm/<token>')
def confirm(token):
    try:
        serializer=URLSafeTimedSerializer(secret_key)
        data=serializer.loads(token,salt=salt,max_age=180)
    except Exception as e:
        return 'link expried'
    else:
        user=data['username']
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select count(*) from register where username=%s',[user])
        count=cursor.fetchone()[0]
        if count==1:
            cursor.close()
            flash('The user name is already exists')
            return redirect(url_for('registration'))
        else:
            cursor.execute('insert into register values(%s,%s,%s)',[user,data['password'],data['email']])
            mydb.commit()
            cursor.close()
            flash('Details has successfully registered')
            return redirect(url_for('login'))
@app.route('/login',methods=['GET','POST'])
def login():
    if session.get['user']:
      return redirect(url_for('home'))
    if request.method=='POST':
        user=str(request.form['username'])
        password=int(request.form['password'])
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select count(*) from register where username=%s and password=%s')
        if count==1:
          session['user']=user
          flash('success')
          return redirect(url_for('home'))
        else:
          flash('invalid')
          return redirect(url_for('login'))
    else:
        return render_template('login.html')
@app.route('/homepage')
def home():
  if session.get('user'):
    return render_template('homepage.html')
  else:
    return redirect(url_for('login'))
@app.route('/logout')
def logout():
  if session.get('user'):
    session.pop('user')
    flash('logged out')
    return redirect(url_for('login'))
  return redirect(url_for('login'))
app.run(debug=True,use_reloader=True)





