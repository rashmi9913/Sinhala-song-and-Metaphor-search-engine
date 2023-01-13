def basic_search_query(query):
    res = {
        "size": 150,
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["Title.case_insensitive_and_inflections", "Lyrics", "Metaphors.Metaphor", "Metaphors.Interpretation"],
                "operator": "or",
                "type": "best_fields"
            }
        }
    }
    return res

def artist_filter_search_query(query_filter_artist):
    res = {
        "size": 150,
        "query": {
            "match_phrase": {
                "Artist_si": {
                    "query": query_filter_artist
                }
            }
        }
    }
    return res

def genre_filter_search_query(query_filter_genre):
    res = {
        "size": 150,
        "query": {
            "match_phrase": {
                "Genre_si" : {
                    "query": query_filter_genre
                }
            }
        }
    }
    return res

def songwriter_filter_search_query(query_filter_songwriter):
    res = {
        "size": 150,
        "query": {
            "match_phrase": {
                "Song Writer_si": {
                    "query": query_filter_songwriter
                }
            }
        }
    }
    return res

def composer_filter_search_query(query_filter_composer):
    res = {
        "size": 150,
        "query": {
            "match_phrase": {
                "Music_si": {
                    "query": query_filter_composer
                }
            }
        }
    }
    return res

def source_filter_search_query(query_filter_source):
    res = {
        "size": 150,
        "query": {
            "match_phrase": {
                "Metaphors.Source Domain": {
                    "query": query_filter_source
                }
            }
        }
    }
    return res

def target_filter_search_query(query_filter_target):
    res = {
        "size": 150,
        "query": {
            "match_phrase": {
                "Metaphors.Target Domain": {
                    "query": query_filter_target
                }
            }
        }
    }
    return res

