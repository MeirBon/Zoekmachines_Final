from es_init import get_connection


es = get_connection()
print(es.indices.exists('goeievraag'))