from src.es_init import get_connection, load_data
from flask import Flask, request, render_template, redirect, url_for


app = Flask('goeievraag')
load_data()
es = get_connection()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    return redirect(
        url_for('s', query=str(query))
    )


@app.route('/s/<string:query>')
def s(query):
    return render_template('search.html', query=query)

@app.route('/s_a')
def s_a():
    return str(request.form)
