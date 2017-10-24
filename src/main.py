from src.es_init import get_connection, load_data
from flask import Flask, request, render_template, redirect, url_for

app = Flask('goeievraag')  # start Flask app
es = get_connection()  # get elasticsearch connection


#
#   index route
#
@app.route('/')
def index():
    return render_template('index.html')


#
#   search handler
#
@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    return redirect(
        url_for('s', query=str(query))
    )


#
#   route for simple queries
#
@app.route('/s/<string:query>')
def s(query):
    return render_template('search.html', query=query)


#
#   TODO: route for advanced queries
#
@app.route('/s_a')
def s_a():
    return str(request.form)
