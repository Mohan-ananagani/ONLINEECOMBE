from flask import Flask as f,jsonify as j,request as r,url_for as o,render_template,redirect as t
import requests
app=f(__name__)
@app.route('/')
def index():
    return render_template('home.html')
@app.route('/marks',methods=['GET','POST'])
def mark():
    if r.method=='POST':
        print(r.form)
        print(r.form['name'])
        print(r.form['marks'])
        return render_template('good.html')
    else:
        return render_template('good.html')

'''req of args req of form   voting system'''
app.run(debug=True,use_reloader=True)
