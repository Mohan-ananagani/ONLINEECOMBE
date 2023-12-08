from flask import Flask,redirect,url_for
app=Flask(__name__)
@app.route('/')
def home():
    return 'hello'
@app.route('/two/<name>/<plc>')
def info(name,plc):
    if plc == 'vja':
        return redirect('https://127.0.0.1:5000/dest')
    else:
        return 'hyd'
@app.route('/dest')
def location():
    return 'vja'
app.run(debug=True, use_reloader=True)

'''
def info(name,plc):
    if plc == 'vja':
        return redirect(url_for('location'))
    else:
        return 'hyd'

'''















