from elasticsearch import Elasticsearch
from nltk.corpus import stopwords


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


def advanced_search(es: Elasticsearch, query, category, user_id, from_date, till_date, offset=0, size=20):
    if query and category and user_id and from_date and till_date:
        return es.search(index="goeievraag", doc_type="questions", body={
            "from": offset, "size": size,
            "query": {
                "bool": {
                    "should": [
                        {"multi_match": {
                            "query": query,
                            "fields": ["question", "description"]
                        }},
                        {"match": {"categoryId": category}},
                        {"match": {"userId": user_id}}
                    ],
                    "filter": [
                        {"range": {"date": {"gte": from_date}}},
                        {"range": {"date": {"lte": till_date}}},
                    ]
                }
            }
        })
    elif query and category and user_id and from_date:
        return es.search(index="goeievraag", doc_type="questions", body={
            "from": offset, "size": size,
            "query": {
                "bool": {
                    "should": [
                        {"multi_match": {
                            "query": query,
                            "fields": ["question", "description"]
                        }},
                        {"match": {"categoryId": category}},
                        {"match": {"userId": user_id}}
                    ],
                    "filter": [
                        {
                            "range": {
                                "date": {
                                    "gte": from_date
                                }
                            }
                        }
                    ]
                }
            }
        })
    elif query and from_date and till_date:
        return es.search(index="goeievraag", doc_type="questions", body={
            "from": offset, "size": size,
            "query": {
                "bool": {
                    "should": {
                        "multi_match": {
                            "query": query,
                            "fields": ["question", "description"]
                        }
                    },
                    "filter": [
                        {
                            "range": {
                                "date": {
                                    "gte": from_date,
                                    "lte": till_date
                                }
                            }
                        }
                    ]
                }
            }
        })
    elif query and from_date:
        return es.search(index="goeievraag", doc_type="questions", body={
            "from": offset, "size": size,
            "query": {
                "bool": {
                    "should": [
                        {"multi_match": {
                            "query": query,
                            "fields": ["question", "description"]
                        }}
                    ],
                    "filter": [
                        {"range": {"date": {"gte": from_date}}}
                    ]
                }
            }
        })
    elif query and till_date:
        return es.search(index="goeievraag", doc_type="questions", body={
            "from": offset, "size": size,
            "query": {
                "bool": {
                    "should": [
                        {"multi_match": {
                            "query": query,
                            "fields": ["question", "description"]
                        }}
                    ],
                    "filter": [
                        {"range": {"date": {"lte": till_date}}}
                    ]
                }
            }
        })
    elif query and category and user_id and till_date:
        return es.search(index="goeievraag", doc_type="questions", body={
            "from": offset, "size": size,
            "query": {
                "bool": {
                    "should": [
                        {"multi_match": {
                            "query": query,
                            "fields": ["question", "description"]
                        }},
                        {"match": {"categoryId": category}},
                        {"match": {"userId": user_id}}
                    ],
                    "filter": [
                        {"range": {"date": {"lte": till_date}}},
                    ]
                }
            }
        })
    elif query and category and user_id:
        return es.search(index="goeievraag", doc_type="questions", body={
            "from": offset, "size": size,
            "query": {
                "bool": {
                    "should": [
                        {"multi_match": {
                            "query": query,
                            "fields": ["question", "description"]
                        }}
                    ],
                    'must': [
                        {"match": {"userId": user_id}},
                        {"match": {"categoryId": category}}
                    ]
                }
            }
        })
    elif query and user_id:
        return es.search(index="goeievraag", doc_type="questions", body={
            "from": offset, "size": size,
            "query": {
                "bool": {
                    "should": [
                        {"multi_match": {
                            "query": query,
                            "fields": ["question", "description"]
                        }}
                    ],
                    'must': [
                        {"match": {"userId": user_id}}
                    ]
                }
            }
        })
    elif query and category:
        return es.search(index="goeievraag", doc_type="questions", body={
            "from": offset, "size": size,
            "query": {
                "bool": {
                    "should": [
                        {"multi_match": {
                            "query": query,
                            "fields": ["question", "description"]
                        }},
                        {"match": {"categoryId": category}}
                    ]
                }
            }
        })
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


def get_question(es: Elasticsearch, question_id):
    return es.get(index="goeievraag", doc_type="questions", id=question_id)


def get_answers(es: Elasticsearch, question_id):
    return es.search(index="goeievraag", doc_type="answers", body={
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


def get_categories(es: Elasticsearch):
    return es.search(index="goeievraag", doc_type="categories", body={
        "size": 1000,
        "query": {
            "match_all": {}
        }
    })


def get_termvectors(es: Elasticsearch, id):
    result = es.termvectors(index="goeievraag", doc_type="questions", id=id, body={
        "fields": ["question", "description"],
    })

    stop = set(stopwords.words('dutch'))
    vectors = dict()

    for term, data in result['term_vectors']['question']['terms'].items():
        if term in stop:
            continue
        if term not in vectors:
            vectors[term] = data['term_freq']
        else:
            vectors[term] += data['term_freq']

    for term, data in result['term_vectors']['description']['terms'].items():
        if term in stop:
            continue
        if term not in vectors:
            vectors[term] = data['term_freq']
        else:
            vectors[term] += data['term_freq']

    return vectors
