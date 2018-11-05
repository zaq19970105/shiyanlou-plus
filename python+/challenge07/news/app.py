import os
import json
from flask import Flask
from flask import render_template, abort
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/myDB'

db = SQLAlchemy(app)

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    created_time = db.Column(db.DateTime)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    content = db.Column(db.Text)

    def __init__(self, title, category, content):
        self.title = title
        self.created_time = datetime.datetime.utcnow()
        self.category_id = category.id
        self.content = content

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

@app.route('/files/<file_id>')
def file(file_id):
    f = File.query.filter_by(title=file_id).first()

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

create_data()
if __name__ == '__main__':
    app.run(debug=1)
