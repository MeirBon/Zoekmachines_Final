from src.es_init import get_connection, load_data
from flask import Flask, request, render_template, redirect, url_for
from src.search import simple_search, advanced_search, get_question, get_answers, get_categories
import time

app = Flask('goeievraag')  # start Flask app
es = get_connection()  # get elasticsearch connection


#
#   index route
#
@app.route('/')
def index():
    return render_template('index.html', advanced=False)


#
#   advanced search index
#
@app.route('/advanced', methods=['GET', 'POST'])
def advanced_index():
    return render_template('index.html', advanced=True, categories=get_categories(es))


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
    current_page = int(request.args.get('page', 1))
    offset = current_page * 20 - 20

    time1 = time.time()
    results = simple_search(es, query, offset)
    elapsed = round(time.time() - time1, 10)

    pages = round(results['hits']['total'] / 20)

    if results['hits']['total'] % 20 > 0:
        pages += 1
    return render_template('search.html', query=query, advanced=False,
                           results=results, elapsed=elapsed,
                           pages=pages, current_page=current_page)


#
#   route for details of question
#
@app.route('/question/<int:question_id>')
def question(question_id):
    data = get_question(es, question_id)
    answers = get_answers(es, question_id)
    return render_template('question.html', data=data, answers=answers)


#
#   TODO: route for advanced queries
#
@app.route('/s_a')
def s_a():
    current_page = int(request.args.get('page', 1))
    offset = current_page * 20 - 20

    query = request.args.get('query', '')
    user_id = request.args.get('userId', '')
    from_date = request.args.get('from', '')
    till_date = request.args.get('till', '')
    category = request.args.get('category', '')
    if category is 1 or category is '1':
        category = ''

    time1 = time.time()
    results = advanced_search(es, offset=offset, query=query, category=category, user_id=user_id, from_date=from_date, till_date=till_date)
    elapsed = round(time.time() - time1, 10)

    pages = round(results['hits']['total'] / 20)
    if results['hits']['total'] % 20 > 0:
        pages += 1

    return render_template('search.html', query=query, advanced=True,
                           results=results, elapsed=elapsed,
                           pages=pages, current_page=current_page)
