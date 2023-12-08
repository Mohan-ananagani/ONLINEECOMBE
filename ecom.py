from flask import Flask,request,render_template,url_for,redirect,flash,abort,session
import mysql.connector
from flask_session import Session
from itsdangerous import URLSafeTimedSerializer
from stoken import token
from key import secret_key,salt,salt2,salt3
from cmail import sendmail
from otp import adotp
import os
from io import BytesIO
mydb=mysql.connector.connect(host='localhost',user='root',password='Admin',db='ecommerce')
app=Flask(__name__)
app.secret_key=secret_key
app.config['SESSION_TYPE']='filesystem'
@app.route('/')
def index():
    return render_template('welcome.html')
@app.route('/homepage')
def home():
    if session.get('user'):
        return render_template('home1.html')
    return render_template('home1.html')
@app.route('/signup',methods=['GET','POST'])
def usignup():
    if request.method=='POST':
        user=request.form['name']
        mobile=request.form['mobile']
        email=request.form['email']
        address=request.form['address']
        gender=request.form['gender']
        password=request.form['password']
        try:
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select count(*) from users where email=%s',[email])
            count=cursor.fetchone()[0]
            print(count)
            if count==1:
                raise Exception
        except Exception as e:
            flash('User alredy registered')
            return redirect(url_for('home'))
        else:
            data={'user':user,'email':email,'mobile':mobile,'address':address,'gender':gender,'password':password}
            subject='The confirmation link has sent to Email'
            body=f"Click the link to confirm{url_for('confirm',token=token(data,salt=salt),_external=True)}"
            sendmail(to=email,subject=subject,body=body)
            flash('Link has sent to this Mail')
            return redirect(url_for('login'))
    return render_template('signup.html')
@app.route('/login',methods=['GET','POST'])
def login():
    if session.get('user'):
        return redirect(url_for('home'))
    if request.method=='POST':
        user=request.form['username']
        password=request.form['password']
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select user_name,password from users where user_name=%s and password=%s',[user,password])
        count=cursor.fetchone()
        if count==(user,password):
            session['user']=user
            return redirect(url_for('home'))
    return render_template('login.html')
@app.route('/confirm/<token>')
def confirm(token):
    try:
        serializer=URLSafeTimedSerializer(secret_key)
        data=serializer.loads(token,salt=salt,max_age=180)
    except Exception as e:
        abort(404,'Link expired')
    else:
        cursor=mydb.cursor(buffered=True)
        cursor.execute('insert into users(user_id,user_name,u_mobile,email,gender,address,password) values(uuid_to_bin(uuid()),%s,%s,%s,%s,%s,%s)',[data['user'],data['mobile'],data['email'],data['gender'],data['address'],data['password']])
        mydb.commit()
        cursor.close()
        flash('Details Registered successfully')
        return redirect(url_for('login'))
@app.route('/logout')
def logout():
    if session.get('user'):
        session.pop('user')
        return redirect(url_for('login'))
    return redirect(url_for('login'))
@app.route('/forgot',methods=['GET','POST'])
def forgot():
    if request.method=='POST':
        email=request.form['id']
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select count(*) from users where email=%s',[email])
        count=cursor.fetchone()[0]
        cursor.close()
        try:
            if count!=1:
                raise Exception
        except Exception as e:
            flash('Pls Register for the application')
            return redirect(url_for('index'))
        else:
            subject='Reset link for ecom application'
            body=f"The reset link for ecom application: {url_for('uforgot',token=token(email,salt=salt2),_external=True)}"
            sendmail(to=email,subject=subject,body=body)
            flash('Reset Link has sent to give email pls check.')
            return redirect(url_for('forgot'))
    return render_template('forgot.html')
@app.route('/uforgot/<token>',methods=['GET','POST'])
def uforgot(token):
    try:
        serializer=URLSafeTimedSerializer(secret_key)
        data=serializer.loads(token,salt=salt2,max_age=180)
    except:
        abort(404,'Reset link expired')
    else:
        if request.method=='POST':
            npassword=request.form['npassword']
            cpassword=request.form['cpassword']
            if npassword==cpassword:
                cursor=mydb.cursor(buffered=True)
                cursor.execute('update users set password=%s where email=%s',[npassword,data])
                mydb.commit()
                cursor.close()
                flash('Password has updated')
                return redirect(url_for('login'))
            else:
                flash('Mismatched  confirmation password')
                return render_template('newpassword.html')
        return render_template('newpassword.html')
@app.route('/admincreate',methods=['GET','POST'])
def admincreate():
    if request.method=='POST':
        a_id=adotp()
        admin=request.form['name']
        aemail=request.form['email']
        amobile=request.form['mobile']
        password=request.form['password']
        try:
            cursor=mydb.cursor(buffered=True)
            print('hi')
            cursor.execute('select count(*) from ad where admin_email=%s',[aemail])
            count=cursor.fetchone()[0]
            print(count)
            if count==1:
                raise Exception
        except Exception as e:
            flash('User alredy existed')
            return redirect(url_for('index'))
        else:
            serializer=URLSafeTimedSerializer(secret_key)
            data=serializer.dumps(a_id,salt=salt3)
            subject='OTP for ecom application'
            body=f"This is the otp for your account creation: {a_id}"
            sendmail(to=aemail,subject=subject,body=body)
            flash('The otp has sent to given mail')
            return redirect(url_for('adminverify',data=data,admin=admin,aemail=aemail,amobile=amobile,password=password))
        
    return render_template('adminsignup.html') 
@app.route('/adminverify/<data>/<admin>/<aemail>/<amobile>/<password>',methods=['GET','POST'])
def adminverify(data,admin,aemail,amobile,password):
    try:
        serializer=URLSafeTimedSerializer(secret_key)
        otp=serializer.loads(data,salt=salt3,max_age=180)
        
    except:
        abort(404,'OTP has expired')
    else:
        if request.method=='POST':
            print(otp)
            uotp=request.form['adminotp']
            print(uotp)
            if otp==uotp:
                cursor=mydb.cursor(buffered=True)
                cursor.execute('insert into ad(admin_id,admin_name,admin_mobile,admin_email,password) values(%s,%s,%s,%s,%s)',[uotp,admin,amobile,aemail,password])
                mydb.commit()
                cursor.close()
                flash('Details Registered successfully')
                return redirect(url_for('adminlogin'))
    return render_template('adminotp.html')
@app.route('/adminlogin',methods=['GET','POST'])
def adminlogin():
    if session.get('user'):
        return redirect(url_for('admindashboard'))
    if request.method=='POST':
        auser=request.form['email']
        password=request.form['password']
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select admin_email,password from ad where admin_email=%s and password=%s',[auser,password])
        count=cursor.fetchone()
        if count==(auser,password):
            session['user']=auser
            return redirect(url_for('admindash'))
    return render_template('adminlogin.html')
@app.route('/aforgot',methods=['GET','POST'])
def aforgot():
    if request.method=='POST':
        email=request.form['id']
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select count(*) from ad where admin_email=%s',[email])
        count=cursor.fetchone()[0]
        cursor.close()
        try:
            if count!=1:
                raise Exception
        except Exception as e:
            flash('Pls Register for the application')
            return redirect(url_for('index'))
        else:
            subject='Admin Reset link for ecom application'
            body=f"The reset link for ecom application: {url_for('averify',token=token(email,salt=salt2),_external=True)}"
            sendmail(to=email,subject=subject,body=body)
            flash('Reset Link has sent to give email pls check.')
            return redirect(url_for('aforgot'))
    return render_template('adminforgot.html')
@app.route('/averify/<token>',methods=['GET','POST'])
def averify(token):
    try:
        serializer=URLSafeTimedSerializer(secret_key)
        data=serializer.loads(token,salt=salt2,max_age=180)
    except:
        abort(404,'Reset link expired')
    else:
        if request.method=='POST':
            npassword=request.form['npassword']
            cpassword=request.form['cpassword']
            if npassword==cpassword:
                cursor=mydb.cursor(buffered=True)
                cursor.execute('update admindetails set password=%s where admin_email=%s',[npassword,data])
                mydb.commit()
                cursor.close()
                flash('Password has updated')
                return redirect(url_for('adminlogin'))
            else:
                flash('Mismatched  confirmation password')
                return render_template('adminnewpassword.html')
    return render_template('adminnewpassword.html')
@app.route('/admindashboard')
def admindash():
    return render_template('admindashboard.html')
@app.route('/alogout')
def alogout():
    if session.get('user'):
        session.pop('user')
        return redirect(url_for('adminlogin'))
    return redirect(url_for('login'))
@app.route('/additems',methods=['GET','POST'])
def additems():
    if session.get('user'):
        if request.method=='POST':
            item_name=request.form['name']
            desc=request.form['desc']
            qyt=request.form['qty']
            category=request.form['category']
            price=request.form['price']
            image=request.files['image']
            addedby=session.get()
            filename=adotp()+'.jpg'
            path = os.path.dirname(os.path.abspath(__file_))
            static_path = os.path.join(path,'static')
            image.save(os.path.join(static_path,filename))
            cursor=mydb.cursor(buffered=True)
            cursor.execute('insert in to additems values(uuid_to_bin(uuid()),%s,%s,%s,%s,%s,%s)')
            mydb.commit()
            cursor.close()
            flash('success')
            return redirec(url_for('additems'))
    return render_template('items.html')
@app.route('/pstatus')
def pstatus():
    if session.get('user'):
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select item_id,item_name,dis,qyt,category,price from additems where item addedby=%s',[session.get('user')])
        items=cursor.fetchall()
        cursor.close()
    return render_template('status.html',items=items)
@app.route('/updata/<itemid>',methods=['GET','POST'])
def update():
    if session.get('user'):
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select item_name,dis,qyt,category,price from')
        mydb.fetchone()
        cursor.close()
        if request.method=='POST':
            item_name=request.form['name']
            desc=request.form['desc']
            qyt=request.form['qty']
            category=request.form['category']
            price=request.form['price']
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select item_name,dis,qyt,category,price from')
            mydb.fetchone()
            cursor.close()
@app.route('/delete/<itemid>',methods=['GET','POST'])
def delete():
app.run(debug=True,use_reloader=True,port=8000)





















































