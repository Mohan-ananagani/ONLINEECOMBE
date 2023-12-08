'''req of args req of form   voting system'''
from flask import Flask as f,render_template as r,request as e,redirect as i,url_for as u
import requests
app = f(__name__)
@app.route('/')
def home():
    return r('voter_home.html')
@app.route('/one',methods=['GET','POST'])
def one():
    if r.method=='POST':
        print(r.form)
        a = r.form['name']
        b = r.form['address']
        c = r.form['phone_number']
        d = r.form['email']
        g = r.form['aadhar_u_id']
        h = r.form['dateOfBirth']
        return i(u('two',a=a,b=b,c=c,d=d,g=g,h=h))
    else:
        return render_template('voter_one.html')
@app.route('/two',methods=['GET'])
def two(a,b,c,d,g,h):
    return render_template('voter_two.html')
app.run(debug=True, use_reloader=True)
