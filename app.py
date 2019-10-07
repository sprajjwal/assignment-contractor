from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from datetime import datetime

# host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/contractor')
# client = MongoClient(host=f'{host}?retryWrites=false')
# db = client.get_default_database()
client = MongoClient()
db = client.contractor
items = db.items


app = Flask(__name__)

@app.route('/')
def store_index():
    """Show all playlists."""
    return render_template('store_index.html', items=items.find())

@app.route('/items', methods=['POST'])
def add_item():
    """Create and add a new item to the database"""
    item = {
        'name': request.form.get('name'),
        'price': request.form.get('price'),
        'in_stock': request.form.get('in'),
        'images': request.form.get('images').split()
    }
    item_id = items.insert_one(item).inserted_id
    return redirect(url_for('item', item_id=item_id))

@app.route('/items/new')
def items_new():
    return render_template('items_new.html', item={}, title='New Item')

# @app.route('/items')
# def store_items():
#     return render_template('items.html', items=items.find())

@app.route('/items/<item_id>')
def item(item_id):
    item = items.find_one({'_id': ObjectId(item_id)})
    return render_template('item.html', item=item)

if __name__ == '__main__':
    # playlists.delete_many({})
    # comments.delete_many({})
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
