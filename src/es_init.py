from os import listdir
from os.path import isfile, join, exists
import json
import datetime
import csv
from elasticsearch import Elasticsearch


def get_mappings():
    folder = join('mappings')
    mappings = [join(folder, file) for file in listdir(folder)
                if isfile(join(folder, file))]
    return mappings


def get_connection(host='127.0.0.1', port=9200,
                   username=None, password=None) -> Elasticsearch:
    # format url for elasticsearch connection
    if exists(join('config.json')):
        with open(join('config.json')) as config_f:
            config = json.loads(config_f.read())
        if config['username'] is None or config['password'] is None:
            url = config['host'] + ':' + config['port']
        else:
            url = config['username'] + ':' + config['password'] + '@' + config['host'] + ':' + config['port']
    elif username is None and password is None:
        url = host + ':' + str(port)
    else:
        url = username + ':' + password + '@' + host + ':' + str(port)

    # init and check if ES is up
    es = Elasticsearch(hosts=[url])
    if not es.ping():
        raise ConnectionError('ElasticSearch is down')

    # init mappings with indices
    print('Initializing mappings in ES')
    for mapping in get_mappings():
        with open(mapping, 'r') as map_f:
            m = json.loads(map_f.read())
        if not es.indices.exists(m['template']):
            es.indices.create(index=m['template'], body=m)
    return es


def to_boolean(value):
    if int(value) == 1:
        return True
    return False


def load_answers(es: Elasticsearch, data_f):
    with open(data_f, 'r', encoding="utf8") as csvfile:  # open data file
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')  # setup reader with delimiter
        for row in reader:  # loop over rows in csv
            if len(row) is not 8:  # check if row is valid
                continue
            try:  # try to setup the data for Elasticsearch, if it fails just continue with the next row
                index = int(row[0])
                if es.exists('goeievraag', 'answers', index):  # if data already loaded into elasticsearch -> continue
                    continue
                data = {  # create json payload
                    "answerId": index,
                    "date": datetime.datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S'),
                    "userId": int(row[2]),
                    "questionId": int(row[3]),
                    "answer": str(row[4]),
                    "thumbsDown": int(row[5]),
                    "thumbsUp": int(row[6]),
                    "isBestAnswer": to_boolean(row[7])
                }
            except ValueError:
                print('Invalid answer', row[0])  # log to command line which answers are invalid
                continue
            es.create('goeievraag', 'answers', index, data)  # send data to elasticsearch


def load_questions(es: Elasticsearch, data_f):
    with open(data_f, 'r', encoding="utf8") as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            if len(row) is not 6:
                continue
            try:
                index = int(row[0])
                if es.exists('goeievraag', 'questions', index):
                    continue
                data = {
                    "questionId": index,
                    "date": datetime.datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S'),
                    "userId": int(row[2]),
                    "categoryId": int(row[3]),
                    "question": str(row[4]),
                    "description": str(row[5])
                }
            except ValueError:
                print('Invalid question', row[0])
                continue
            es.create('goeievraag', 'questions', index, data)


def load_categories(es: Elasticsearch, data_f):
    with open(data_f, 'r', encoding="utf8") as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            if len(row) is not 3:
                continue
            try:
                index = int(row[0])
                if es.exists('goeievraag', 'categories', index):
                    continue
                data = {
                    "categoryId": index,
                    "parentId": int(row[1]),
                    "category": str(row[2])
                }
            except ValueError:
                print('Invalid categorie', row[0])
                continue
            es.create('goeievraag', 'categories', index, data)


def load_users(es: Elasticsearch, data_f):
    with open(data_f, 'r', encoding="utf8") as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            if len(row) is not 4:
                continue
            try:
                index = int(row[0])
                if es.exists('goeievraag', 'users', index):
                    continue
                data = {
                    "userId": index,
                    "registrationDate": datetime.datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S'),
                    "expertise": str(row[2]),
                    "bestAnswers": int(row[3])
                }
            except ValueError:
                print('Invalid user', row[0])
                continue
            es.create('goeievraag', 'users', index, data)


#
#   Function to load goeievraag data
#
def load_data(es: Elasticsearch):
    print("Loading answers")
    load_answers(es, join('data', 'answers.csv'))
    print("Loading questions")
    load_questions(es, join('data', 'questions.csv'))
    print("Loading categories")
    load_categories(es, join('data', 'categories.csv'))
    print("Loading users")
    load_users(es, join('data', 'users.csv'))
