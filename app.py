from flask import Flask, render_template, request, redirect, jsonify
from model import db, Card, Item
from uuid import uuid4
from pprint import pprint

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home_page():
    button_clicked = None
    if request.method == 'POST':
        if 'edit-card-name' in request.form:
            button_clicked = request.form.get('card_id')
        elif 'edit-item-name' in request.form:
            button_clicked = request.form.get('item_id')
            print("Button clicked:", button_clicked)  # Debug line

    return render_template('index.html', cards=Card.get_all(), button_clicked=button_clicked)

@app.route('/card/new', methods=['POST'])
def add_card():
    name = request.form.get('cardName')
    card_id = str(uuid4())
    Card.create(id=card_id, name=name).save()
    return redirect('/')

@app.route('/item/new', methods=['POST'])
def add_item():
    form = request.form
    card_id = form.get('card_id') # card_id
    name = form.get('name') # name
    Item.create(name=name, card=card_id).save()
    return redirect('/')

@app.route('/item/check', methods=['POST'])
def check_item():
    form = request.form
    item_id = form.get('item_id')
    status = bool(form.get('status', type=int)) # bool 0 = False, >0 = True
    Item.update({Item.completed: status}).where(Item.id == item_id).execute()
    return redirect('/')

@app.route('/card/update', methods=['POST'])
def update_card():
    try:
        card_id = request.form.get('card_id')
        card_name = request.form.get('card_name')
        Card.update({Card.name: card_name}).where(Card.id == card_id).execute()

        print(jsonify(success=True))
        return redirect('/')
    except Exception as e:
        return jsonify(success=False, error=str(e)), 500


@app.route('/item/update', methods=['POST'])
def update_item():
    try:
        item_id = request.form.get('item_id')
        item_name = request.form.get('item_name')
        Item.update({Item.name: item_name}).where(Item.id == item_id).execute()
        return redirect('/')
    except Exception as e:
        return jsonify(success=False, error=str(e)), 500

@app.route('/card/delete', methods=['POST'])
def delete_card():
    card_id = request.form.get('card_id')
    pprint(card_id)
    # delete all items in the card
    Item.delete().where(Item.card_id == card_id).execute()
    # delete Card
    Card.delete().where(Card.id == card_id).execute()
    return redirect('/')

@app.route('/item/delete', methods=['POST'])
def delete_item():
    item_id = request.form.get('item_id')
    # delete item
    Item.delete().where(Item.id == item_id).execute()
    return redirect('/')

if __name__ == ("__main__"):
    db.connect()
    db.create_tables([Card, Item], safe=True)
    app.run('0.0.0.0', port=5000)