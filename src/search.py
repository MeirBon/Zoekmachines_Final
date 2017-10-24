from elasticsearch import Elasticsearch


def simple_search(es: Elasticsearch, query: str, offset=0, size=20):
    return es.search(index="goeievraag", doc_type="questions", body={
        "from": offset, "size": size,
        "query": {
            "bool": {
                "should": {
                    "multi_match": {
                        "query": query,
                        "fields": ["question", "description"]
                    }
                }
            }
        }
    })


def advanced_search(es: Elasticsearch, offset=0, size=20):
    return es.search(index="goeievraag", doc_type="questions", body={
        "from": offset, "size": size
    })


def get_question(es: Elasticsearch, question_id):
    return es.get(index='goeievraag', doc_type='questions', id=question_id)


def get_answers(es: Elasticsearch, question_id):
    return es.search(index='goeievraag', doc_type='answers', body={
        "size": 1000,
        "query": {
            "bool": {
                "must": {
                    "match": {
                        "questionId": question_id
                    }
                }
            }
        }
    })
