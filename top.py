from flask import Flask as f,jsonify as j,request as r
import requests
app=f(__name__)
md=[{'name':'mohan','id':1,'status':'not working'},
    {'name':'mohanan','id':2,'status':'not working'},
    {'name':'mohananagani','id':3,'status':'not working'}]
@app.route('/')
def home():
    return 'hi'
@app.route('/fit',methods=['GET'])
def new():
    return j(md)
@app.route('/adda',methods=['GET','POST'])
def add():
    quote=r.get_json()
    print(quote)
    inc = md[-1]['id']+1
    quote['id'] = inc
    md.append(quote)
    return j(md)
@app.route('/upto/<int:id>',methods=['PUT','GET'])
def updater(id):
    quote=r.get_json()
    for i in md:
        if i['id'] == id:
            i['name'] = quote['name']
            i['status'] = quote['status']
    return j(quote)
@app.route('/det/<int:id>',methods=['DELETE'])
def deleter(id):
    quote=r.get_json()
    for i in md:
        if i['id'] == id:
            md.remove(i)
    return j(quote)
app.run(debug=True, use_reloader=True)
