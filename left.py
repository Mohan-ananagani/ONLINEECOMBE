from flask import Flask,render_template,request,redirect,url_for
app=Flask(__name__)
@app.route('/')
def home():
    return 'board'
@app.route('/marks',methods=['GET','POST'])
def marks():
    if request.method=='POST':
        print(request.form)
        n = request.form['name']
        p = int(request.form['python'])
        m = int(request.form['java'])
        d = int(request.form['marks'])
        total = p + m + d
        
        return render_template('r.html',p=grade,m=total,n=n,d=result,t=p,q=m,s=d)
    else:
        return render_template('g.html')
app.run(debug=True,use_reloader=True)
