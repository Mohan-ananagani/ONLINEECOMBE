from flask import Flask
app=Flask(__name__)
@app.route('/')
def home():
    return f'hello world'
@app.route('/first')
def firs():
     return 'good man'
app.run(debug=True)
