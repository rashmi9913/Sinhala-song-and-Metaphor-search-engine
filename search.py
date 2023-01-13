from elasticsearch import Elasticsearch
from query import basic_search_query, artist_filter_search_query, genre_filter_search_query, songwriter_filter_search_query, composer_filter_search_query, source_filter_search_query, target_filter_search_query

es_client = Elasticsearch(HOST="http://localhost", PORT=9200, http_auth=('username', 'password'))
INDEX = "name_of_the_index"

def basic_search(query_search):
    query_body = basic_search_query(query_search)
    print('Making Basic Search')
    res = es_client.search(index=INDEX, body=query_body)
    return res

def artist_filter_search(query_filter_artist):
    query_body = artist_filter_search_query(query_filter_artist)
    print('Making Artist Filter Search')
    res = es_client.search(index=INDEX, body=query_body)
    return res

def genre_filter_search(query_filter_genre):
    query_body = genre_filter_search_query(query_filter_genre)
    print('Making Genre Filter Search')
    res = es_client.search(index=INDEX, body=query_body)
    return res

def songwriter_filter_search(query_filter_songwriter):
    query_body = songwriter_filter_search_query(query_filter_songwriter)
    print('Making Song Writer Filter Search')
    res = es_client.search(index=INDEX, body=query_body)
    return res

def composer_filter_search(query_filter_composer):
    query_body = composer_filter_search_query(query_filter_composer)
    print('Making Composer Filter Search')
    res = es_client.search(index=INDEX, body=query_body)
    return res

def source_filter_search(query_filter_source):
    query_body = source_filter_search_query(query_filter_source)
    print('Making Source Domain Filter Search')
    res = es_client.search(index=INDEX, body=query_body)
    return res

def target_filter_search(query_filter_target):
    query_body = target_filter_search_query(query_filter_target)
    print('Making Target Domain Filter Search')
    res = es_client.search(index=INDEX, body=query_body)
    return res


