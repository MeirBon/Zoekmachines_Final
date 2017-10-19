from os import listdir
from os.path import isfile, join, exists
import json
from elasticsearch import Elasticsearch


def get_mappings():
    folder = join('..', 'mappings')
    mappings = [join(folder, file) for file in listdir(folder) if isfile(join(folder, file))]
    return mappings


def get_connection(host='127.0.0.1', port=9200,
                   username='elastic', password='changeme')->Elasticsearch:

    # format url
    if exists(join('..', 'config.json')):
        with open(join('..', 'config.json')) as config_f:
            config = json.loads(config_f.read())
        url = config['username'] + ':' + config['password'] + '@' + config['host'] + ':' + config['port']
    else:
        url = username + ':' + password + '@' + host + ':' + str(port)

    # init and check if ES is up
    es = Elasticsearch(hosts=[url])
    if not es.ping():
        raise ConnectionError('ElasticSearch is down')

    # init mappings with indices
    for mapping in get_mappings():
        with open(mapping, 'r') as map_f:
            m = json.loads(map_f.read())
        if not es.indices.exists(m['template']):
            es.indices.create(index=m['template'], body=m)
    return es
