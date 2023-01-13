from elasticsearch import Elasticsearch, helpers
from elasticsearch_dsl import Index
import json

es_client = Elasticsearch(HOST="http://localhost", PORT=9200, http_auth=('username', 'password'))
INDEX = "name_of_the_index"

# define mappings and configs

configs = {
    "settings" : {
        "index" : {
            "analysis" : {
            "analyzer" : {
                "plain" : {
                "filter" : [],
                "tokenizer" : "standard"
                },
                "case_insensitive" : {
                "filter" : ["lowercase"],
                "tokenizer" : "standard"
                },
                "inflections" : {
                  "filter" : ["porter_stem"],
                  "tokenizer" : "standard"
                },
                "case_insensitive_and_inflections" : {
                  "filter" : ["lowercase", "porter_stem"],
                  "tokenizer" : "standard"
                }
            }
          }
        }
    },
    "mappings": {
        "properties": {
            "Title": {
              "type": "text",
              "analyzer": "plain",
              "fields": {
                "case_insensitive": {
                  "type":  "text",
                  "analyzer": "case_insensitive"
                },
                "inflections": {
                  "type":  "text",
                  "analyzer": "inflections"
                },
                "case_insensitive_and_inflections": {
                  "type":  "text",
                  "analyzer": "case_insensitive_and_inflections"
                }
              }
            },
            "Artist_en": {
              "type": "text",
              "analyzer": "plain",
              "fields": {
                "case_insensitive": {
                  "type":  "text",
                  "analyzer": "case_insensitive"
                },
                "inflections": {
                  "type":  "text",
                  "analyzer": "inflections"
                },
                "case_insensitive_and_inflections": {
                  "type":  "text",
                  "analyzer": "case_insensitive_and_inflections"
                }
              }
            },
	          "Artist_si": {
              "type": "text",
              "analyzer": "plain",
              "fields": {
                "inflections": {
                  "type":  "text",
                  "analyzer": "inflections"
                }
              }
            },
	          "Genre_en": {
              "type": "text",
              "analyzer": "plain",
              "fields": {
                "case_insensitive": {
                  "type":  "text",
                  "analyzer": "case_insensitive"
                },
                "inflections": {
                  "type":  "text",
                  "analyzer": "inflections"
                },
                "case_insensitive_and_inflections": {
                  "type":  "text",
                  "analyzer": "case_insensitive_and_inflections"
                }
              }
            },
	          "Genre_si": {
              "type": "text",
              "analyzer": "plain",
              "fields": {
                "inflections": {
                  "type":  "text",
                  "analyzer": "inflections"
                }
              }
            },
	          "Song Writer_en": {
              "type": "text",
              "analyzer": "plain",
              "fields": {
                "case_insensitive": {
                  "type":  "text",
                  "analyzer": "case_insensitive"
                },
                "inflections": {
                  "type":  "text",
                  "analyzer": "inflections"
                },
                "case_insensitive_and_inflections": {
                  "type":  "text",
                  "analyzer": "case_insensitive_and_inflections"
                }
              }
            },
	          "Song Writer_si": {
              "type": "text",
              "analyzer": "plain",
              "fields": {
                "inflections": {
                  "type":  "text",
                  "analyzer": "inflections"
                }
              }
            },
	          "Music_en": {
              "type": "text",
              "analyzer": "plain",
              "fields": {
                "case_insensitive": {
                  "type":  "text",
                  "analyzer": "case_insensitive"
                },
                "inflections": {
                  "type":  "text",
                  "analyzer": "inflections"
                },
                "case_insensitive_and_inflections": {
                  "type":  "text",
                  "analyzer": "case_insensitive_and_inflections"
                }
              }
            },
	          "Music_si": {
              "type": "text",
              "analyzer": "plain",
              "fields": {
                "inflections": {
                  "type":  "text",
                  "analyzer": "inflections"
                }
              }
            },
	          "Lyrics": {
              "type": "text",
              "analyzer": "plain",
              "fields": {
                "inflections": {
                  "type":  "text",
                  "analyzer": "inflections"
                }
              }
            },
	          "Metaphors.Metaphor": {
              "type": "text",
              "analyzer": "plain",
              "fields": {
                "inflections": {
                  "type":  "text",
                  "analyzer": "inflections"
                }
              }
            },
            "Metaphors.Interpretation": {
              "type": "text",
              "analyzer": "plain",
              "fields": {
                "inflections": {
                  "type":  "text",
                  "analyzer": "inflections"
                }
              }
            },
            "Metaphors.Source Domain": {
              "type": "text",
              "analyzer": "plain",
              "fields": {
                "inflections": {
                  "type":  "text",
                  "analyzer": "inflections"
                }
              }
            },
            "Metaphors.Target Domain": {
              "type": "text",
              "analyzer": "plain",
              "fields": {
                "inflections": {
                  "type":  "text",
                  "analyzer": "inflections"
                }
              }
            },
            "Song ID": {
              "type": "integer"
            }
        }
    }
}

def index():
    res = es_client.indices.create(index=INDEX, body=configs)
    #print(res)

    helpers.bulk(es_client, create_bulk())
    #print(res)


def create_bulk():
    with open("./Data/songs_dataset.json") as json_file:
        json_data_all = json.load(json_file)
    key_list = ["Artist_si","Genre_en","Genre_si","Song Writer_en","Song Writer_si","Music_en","Music_si"]
    for i in range(len(json_data_all)):
        json_data = json_data_all[i]
        for j in range (len(key_list)):
            if key_list[j] not in list(json_data.keys()):
                json_data[key_list[j]] = "Unknown"
        yield {
            "_index": INDEX,
            "_source": {
                "Song ID": json_data['Song ID'],
                "Title": json_data['Title'],
                "Artist_en": json_data['Artist_en'],
                "Artist_si": json_data['Artist_si'],
                "Genre_en": json_data['Genre_en'],
                "Genre_si": json_data['Genre_si'],
                "Song Writer_en": json_data['Song Writer_en'],
                "Song Writer_si": json_data['Song Writer_si'],
                "Music_en": json_data['Music_en'],
                "Music_si": json_data['Music_si'],
                "Lyrics": json_data['Lyrics'],
                "Metaphors": json_data['Metaphors'],
            },
        }


# Call elasticsearch bulk API to create the index
if __name__ == "__main__":
    index()
