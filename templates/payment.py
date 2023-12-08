from flask import Flask,render_template,redirect,request,url_for
import stripe
stripe.api_key="sk_test_51NJbH4SCbhc6R6Ahh8czPvuYChDFeEWqXZaZqcy3zy1pD9eI5prUwFqUc06x9lM96tCSgyxlUMWaLVw61EUcdWMx00qrX4o8GU"
app=Flask(__name__)
@app.route('/')
def index():
    return render_template('item1.html')
@app.route('/pay/<name>/<int:price>',methods=['POST'])
def pay(name,price):
    q=int(request.form['qty'])
    total=price*q
    checkout_session=stripe.checkout.Session.create(
        success_url=url_for('success',item=name,qty=q,total=total,_external=True),
        line_items=[
                {
                    'price_data': {
                        'product_data': {
                            'name': name,
                        },
                        'unit_amount': price*100,
'currency': 'inr',
                    },
                    'quantity': q,
                },
                ],
        mode="payment",)
    return redirect(checkout_session.url)
@app.route('/success/<item>/<qty>/<total>')
def success(item,qty,total):
    return {'name':item,'quantity':qty,'total':total}
app.run(debug=True,use_reloader=True)