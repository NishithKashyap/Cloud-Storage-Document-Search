from flask import Flask, render_template, request, redirect, url_for
from main import *
import sqlite3 as sl

app = Flask(__name__)

# flask function to render the page containing the search word details
@app.route('/data/<word>')
def data(word):
    return render_template('data.html', data = find_word(word))

# function to render the html page containing all the files
@app.route('/files')
def files():
    return render_template('files.html', data = retrieve_all_file())

# function to render the html page containing containing info about a specific file
@app.route('/files/<word>/detail')
def file(word):
    d = retrieve_specific_file(word)
    return render_template('file.html', data = d)
    
# function to render the html page containing the requested file content
@app.route('/files/<word>/content')
def content(word):
    return render_template('content.html', data = retrieve_file_content(word))

# function to render the html page containing based on the input 
@app.route('/', methods = ['GET', 'POST'])
def home_page():
    if request.method == 'POST':
        select = request.form.get('choices-single-defaul')
        if select == 'Word Search':
            return redirect(url_for('data', word = request.form['wrd']))

        elif select == 'Display Files':
            return redirect(url_for('files'))

        elif select == 'Find File':
            return redirect(url_for('file', word = request.form['wrd']))

        elif select == 'Display File Content':
            return redirect(url_for('content', word = request.form['wrd']))

    else:
        return render_template('index.html')

if __name__=='__main__':
    app.run(debug = True)
    establish_connection()
    index_file()