from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from datetime import datetime
import re

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/contractor')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
# client = MongoClient()
# db = client.contractor
items = db.items


app = Flask(__name__)
@app.route('/')
def items_index():
    """Show all items."""
    query = request.args.get('searchbar')
    if not query:
        item_list=items.find().sort("name") #how to sort by name?

    else:
        item_list = items.find({"name": {'$regex': ".*"+ query.lower() +
        ".*" }}).sort("name")
    return render_template('store_index.html', items=item_list)


@app.route('/items', methods=['POST'])
def add_item():
    """Create and add a new item to the database."""
    item = {
        'name': request.form.get('name').lower(),
        'display_name': request.form.get('display_name'),
        'price': request.form.get('price'),
        'in_stock': request.form.get('in_stock'),
        'images': request.form.get('images').split()
    }
    print(item['name'])
    item_id = items.insert_one(item).inserted_id
    return redirect(url_for('item', item_id=item_id))

@app.route('/items/new')
def items_new():
    """ Form to make a new item for the store """
    return render_template('items_new.html', item={}, title='New Item')

@app.route('/items/<item_id>')
def item(item_id):
    """ Displays a single item """
    item = items.find_one({'_id': ObjectId(item_id)})
    return render_template('item.html', item=item)

@app.route('/items/<item_id>', methods=["POST"])
def item_update(item_id):
    """ Update item """
    updated_item = {
        'name': request.form.get('name').lower(),
        'display_name': request.form.get('display_name'),
        'price': request.form.get('price'),
        'in_stock': request.form.get('in_stock'),
        'images': request.form.get('images').split()
    }
    items.update_one(
        {"_id" : ObjectId(item_id)},
        {'$set' : updated_item}
    )
    return redirect(url_for('item', item_id=item_id))

@app.route('/items/<item_id>/edit')
def item_edit(item_id):
    """Show the edit form for an item."""
    item = items.find_one({'_id': ObjectId(item_id)})
    return render_template('item_edit.html', item=item, title='Edit Item')


@app.route('/items/<item_id>/delete', methods=['POST'])
def items_delete(item_id):
    """Delete one playlist."""
    items.delete_one({'_id': ObjectId(item_id)})
    return redirect(url_for('items_index'))


if __name__ == '__main__':
    # items.delete_many({})
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
