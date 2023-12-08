@app.route('/readcontactus')
def readcontactus():
    cursor=mydb.cursor(buffered=True)
    cursor.execute('select * from contactus')
@app.route('/dash/<category>')
def dash(category):
    cursor=mydb.cursor(buffered=True)
    cursor.execute('select bin_to_uuid(item_id),item_name,dis,qyt,category,price from items')
@app.route('/cart')
def dash(category):
    cursor=mydb.cursor(buffered=True)
@app.route('/dis/<itemid>')
def dis(itemid):
    cursor=mydb.cursor(buffered=True)
    cursor.execute("select bin_to_uuid")
    items=cursor.fetchone()
    mysb.commit()
    flash
    return render_t('review.html')
    return render_template('discription.html',items=items)

