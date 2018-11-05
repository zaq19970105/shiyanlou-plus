import os
import json
from flask import Flask
from flask import render_template, abort


app = Flask(__name__)

@app.route('/')
def index():
    titles = []
    for title in os.listdir('../files'):
        titles.append(title)

    return render_template('index.html', titles=titles)

@app.route('/files/<filename>')
def file(filename):
    path = '../files/' + filename + '.json'
    print(path)

    if os.path.exists(path):
        with open(path, 'r') as f:
            data = json.load(f)
        return render_template('file.html', data=data)
    else :
        abort(404)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run()
