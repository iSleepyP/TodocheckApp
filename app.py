from flask import Flask,render_template,request,redirect
from module import db,Card,Item
from uuid import uuid4
from pprint import pprint

app= Flask(__name__)

@app.route('/',methods=["GET"])
def home_page():
    pprint(Card.get_all())
    return render_template('index.html',cards=Card.get_all())

@app.route('/card/new',methods=['POST'])
def add_card():
    name = request.form.get('cardName')
    card_id = str(uuid4())
    Card.create(id=card_id,name=name).save() #create&save in db
    return redirect('/')

@app.route('/item/new',methods=["POST"])
def add_item():
    form = request.form
    card_id = form.get('card_id')#card_id
    name = form.get('name')#name
    Item.create(name=name,card=card_id).save()
    return redirect('/')

@app.route('/item/check',methods=['POST'])
def check_item():
    form = request.form
    item_id = form.get('item_id')
    status = bool(form.get('status',type=int)) #bool(0) = false bool>0 = true
    Item.update({Item.completed:status}).where(Item.id == item_id).execute() #update status check box ตาม id แล้ว save
    return redirect('/')

if __name__ == "__main__":
    db.connect()
    db.create_tables([Card,Item])
    app.run(debug=True)
    app.run("0.0.0.0",port = 5000)
