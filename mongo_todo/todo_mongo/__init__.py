from flask import Flask, render_template, url_for, redirect, request
from models import mongo
from bson.objectid import ObjectId # The ObjectID will take the ID and convert it to the object ID that mongo can work



app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb+srv://todo2:<password>@cluster0.us7rg.mongodb.net/mydb?retryWrites=true&w=majority'
mongo.init_app(app)



@app.route('/', methods=['POST', 'GET'])
def home():
    todos_collection = mongo.db.todos
    todos = todos_collection.find() # Will get all the items inside the DB
    return render_template('index.html', todos=todos)


@app.route('/add_todo', methods=['POST', 'GET'])
def add():
    todos_collection = mongo.db.todos # Will create our collections
    todo_item = request.form.get('new_todo')
    todos_collection.insert_one({'text' : todo_item, 'complete' : False}) # Will create our documents and fields
    return redirect(url_for('home'))


@app.route('/complete/<todo_id>')
def complete(todo_id):
    todos_collection = mongo.db.todos
    todo_item = todos_collection.find_one({'_id' : ObjectId(todo_id)})
    todos_collection.update_one(todo_item, {'$set' : {'complete' : True}})
    return redirect(url_for('home'))

@app.route('/not_complete/<todo_id>')
def not_completed(todo_id):
    todos_collection = mongo.db.todos
    todo_item = todos_collection.find_one({'_id' : ObjectId(todo_id)})
    todos_collection.update_one(todo_item, {'$set' : {'complete' : False}})
    return redirect(url_for('home'))

@app.route('/delete-completed')
def delete():
    todos_collection = mongo.db.todos
    
    # Will delete all items that have the complete field equal to True
    todos_collection.delete_many({'complete' : True})
    return redirect(url_for('home'))


@app.route('/delete-all')
def delete_all():
    todos_collection = mongo.db.todos
    # If you pass an empty dictionary, it will represent an empty query, which means all items
    todos_collection.delete_many({})
    return redirect(url_for('home'))





if __name__ == '__main__':
    app.debug = True
    app.run()
