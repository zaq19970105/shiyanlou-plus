import os
import json
from flask import Flask
from flask import render_template, abort
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime
from pymongo import MongoClient


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/myDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

client = MongoClient('127.0.0.1', 27017)

dbM = client.myDB.files

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    created_time = db.Column(db.DateTime)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    content = db.Column(db.Text)
    category = db.relationship('Category')

    def __init__(self, title, category, content):
        self.title = title
        self.created_time = datetime.datetime.utcnow()
        self.category = category
        self.content = content

    def add_tag(self, tag_name):
        if not dbM.find_one({'title_id': self.id, 'tags': tag_name}):
            dbM.insert_one({'title_id': self.id, 'tags': tag_name})
        pass

    def remove_tag(self, tag_name):
        if dbM.find_one({'title_id': self.id, 'tags': tag_name}):
            dbM.delete_one({'title_id': self.id, 'tags': tag_name})
        pass

    @property
    def tags(self):
        ts = []
        for t in dbM.find({'title_id': self.id}):
            ts.append(t['tags'])
        return ts
        pass

    def __repr__(self):
        return '<File %r>' % self.title


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return '<Category %r>' % self.name


@app.route('/')
def index():
    files = File.query.all()
    urlP = 'http://localhost:3000/files/'
    return render_template('index.html', urlP=urlP, files=files)

@app.route('/index')
def index1():
    return index()

@app.route('/files/<file_id>')
def file(file_id):
    f = File.query.filter_by(title=file_id).first()
    print(type(f))
    if f:
        return render_template('file.html', article=f)
    else :
        abort(404)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

def create_data():
    db.drop_all()
    db.create_all()
    java = Category('Java')
    python = Category('Python')
    file1 = File('Hello_Java', java, 'File Content - Java is cool!')
    file2 = File('Hello_Python', python, 'File Content - Python is cool!')
    db.session.add(java)
    db.session.add(python)
    db.session.add(file1)
    db.session.add(file2)
    db.session.commit()

    dbM.remove({})
    file1.add_tag('tech')
    file1.add_tag('java')
    file1.add_tag('linux')
    file2.add_tag('tech')
    file2.add_tag('python')


create_data()
if __name__ == '__main__':
    app.run(debug=1)
