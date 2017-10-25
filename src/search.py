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


def advanced_search(es: Elasticsearch, query, category, user_id, from_date, till_date, offset=0, size=20):
    if query == '':
        query = False
    if category == '':
        category = False
    if user_id == '':
        user_id = False
    if from_date == '':
        from_date = False
    if till_date == '':
        till_date = False

    if query and category and user_id and from_date and till_date:
        print('1')
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
        print('2')
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
        print('10')
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
        print('3')
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
        print('4')
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
        print('5')
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
        print('7')
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
    print('8')
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
