from flask import Flask as f,redirect as r,url_for as u,request as e
app=f(__name__)
@app.route('/')
def home():
    return 'home page'
@app.route('/details')
def info():
    print(e.args)
    name = e.args['name']
    age = e.args['age']
    place = e.args['place']
    return r(u('success',n=name,a=age,p=place))
@app.route('/final/<n>/<a>/<p>')
def success(n,a,p):
    return f'{n} {a} {p}'
app.run(debug=True, use_reloader=True)
