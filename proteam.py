from flask import Flask,render_template
app=Flask(__name__)
@app.route('/')
def home():
    return render_template('tp.html')
@app.route('/child')
def child():
    return render_template('child.html')
app.run(debug=True, use_reloader=True)
