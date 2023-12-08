from flask import Flask,render_template,url_for,request,redirect,flash,abort
#pip install mysql-connector-python
from key import secret_key
from mysql.connector
mydb=mysql.connector.connect(host='localhost',user='root',password='Admin',db='ecom')
app=Flask(__name__)
app.secret_key=secret_key
@app.route('/')
def index():
    return render_template('one.html')
@app.route('/home')
def home():
    return render_template('one.html')
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
            flash("user already registered")
            return redirect(url_for('home'))
        else:
            data={'user':user,'email':email,'mobile':mobile,'address':address,'gender':gender,'password':password}
            subject="the confirmation link has sent to Email"
            body=f"click the link to confirm{url_for('confirm',token=token(data,salt),_external}"
            sendmail(to=email,subject=subject,body=body)
            flash("link has sent to this mail")
            return redirect(url_for('login'))
    return render_template('one_sp.html')
@app.route('/login',methods=['GET','POST'])
def login():
    return render_template('one_l.html')
@app.route('/confirm/<token>')
def uconfirm(token):
    try:
        serializer=URLSafeTimedSerializer(secret_key)
        data=serializer.loads(token,salt=salt,max_age=180)
    except Exception as e:
        abort(404,'link expired')
    else:
        cursor=mydb.cursor(buffered=True)
        cursor.execute('insert into users values(uuid_to_bin(uuid()),%s,%s,%s,%s,%s,%s)')
        mydb.commit()
        cursor.close()
        flash('details registered successfully')
        return redirect(url_for('login'))
@app.route('/alogin',methods=['GET','POST'])
def alogin():
    return render_template('one.html')
@app.route('/asignup',methods=['GET','POST'])
def asignup():
    if request.method=='POST':
        a_id = adotp()
        admin=request.form['name']
        email=request.form['email']
        mobile=request.form['mobile']
        password=request.form['password']
        try:
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select count(*) from ad where admin_email=%s',[aemail])
            count=cursor.fetchone()[0]
            cursor.close()
            if count == 1:
                raise Exception
        except Exception as e:
            flash('u r there')
            return redirect(url_for('index'))
        else:
            serializer=URLSafeTimedSerializer(secret_key)
            data=serializer.loads(a_id,salt=salt3)
            subject = 'otp for ecom'
            body=f"{a_id}"
            sendmail(to=email,subject=subject,body=body)
            flash('good')
            return redirect(url_for('toop',data=data,admin=admin,email=email,mobile=mobile,password=password))
    return render_template('one.html')
@app.route('/toop/<data>/<admin>/<email>/<password>/<mobile>',methods=['GET','POST'])
def toop(data,admin,email,password,mobile):
    try:
        serializer=URLSafeTimedSerializer(secret_key)
        data=serializer.loads(data,salt=salt3,max_age=180)
    except Exception as e:
        abort(404,'link expired')
    else:
        if request.method=='POST':
            uotp=request.form['adminotp']
        if otp == uotp:
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select count(*) from ad where admin_email=%s',[aemail])
            count=cursor.fetchone()[0]
            cursor.commit()
            cursor.close()
    return render_template()
@app.route('/forgot',methods=['GET','POST'])
def forgot():
    email = request.form['id']
    cursor=mydb.cursor(buffered=True)
    cursor.execute('select count(*) from users where email=%s',[email])
    count=cursor.fetchone()[0]
    cursor.close()
    try:
        if count != 1:
            raise Exception
    except Exception as e:
        flash('first register')
        return redirect(url_for('login'))
        '''if count==1:
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select e_s from users where email=%s',[email])
            status=cursor.fetchone()[0]
            cursor.close()
            if status != 'confirmed':
                flash('please confirm your email first')
                return render_template('one_fp.html')'''
    else:
        subject='Forgot Password'
        body=f"{url_for('reset',token=token(email,salt=salt2),_external=True)}"
        sendmail(to=email,subject=subject,body=body)
        flash("link has sent to this mail")
        return redirect(url_for('login'))
        '''else:
            flash("invalid email")
            return render_template('one_l.html')'''
    return render_template('one_fp.html')
@app.route('/reset/<token>',methods=['GET','POST'])
def reset(token):
    try:
        serializer=URLSafeTimedSerializer(secret_key)
        data=serializer.loads(token,salt=salt2,max_age=180)
    except Exception as e:
        abort(404,'link expired')
    else:
        if request.method=='POST':
            npass=request.form['npass']
            cpass=request.form['cpass']
            if npass == cpass:
                cursor=mydb.cursor(buffered=True)
                cursor.execute('update users set password=%s where email=%s',[npass,data])
                mydb.commit()
                cursor.close()
                flash('pass update')
                return redirect(url_for('login'))
            else:
                flash('mismatch password')
                return render_template('newpassword.html')
    return render_template('one_nps.html')
@app.route(''.methods=[])
def ():
    return
app.run(debug=True, use_reloader=True)







