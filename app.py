from flask import Flask, render_template, request
from search import basic_search, artist_filter_search, genre_filter_search, songwriter_filter_search, composer_filter_search, source_filter_search, target_filter_search
from elasticsearch_dsl import Index
from ast import literal_eval
import json

import sys
sys.setrecursionlimit(10000)

app = Flask(__name__ , template_folder='./templates', static_folder='./templates')

@app.route('/', methods=['GET', 'POST'])
def main():
    data = get_data()
    if request.method == 'POST':
        query_search = request.form['searchTerm']
        if query_search == None:
            query_search = data['query_search']
        query_filter_artist = request.form['filterinput-artist']
        if query_filter_artist == "":
            query_filter_artist = data['query_filter_artist']
        elif query_filter_artist == "-":
            query_filter_artist = "Enter Artist Name..."
        query_filter_genre = request.form['filterinput-genre']
        if query_filter_genre == "":
            query_filter_genre = data['query_filter_genre'] 
        elif query_filter_genre == "-":
            query_filter_genre = "Enter Genre..."
        query_filter_songwriter = request.form['filterinput-songwriter']
        if query_filter_songwriter == "":
            query_filter_songwriter = data['query_filter_songwriter']
        elif query_filter_songwriter == "-":
            query_filter_songwriter = "Enter Song Writer Name..."
        query_filter_composer = request.form['filterinput-composer']
        if query_filter_composer == "":
            query_filter_composer = data['query_filter_composer']
        elif query_filter_composer == "-":
            query_filter_composer = "Enter Composer Name..."
        query_filter_source = request.form['filterinput-source']
        if query_filter_source == "":
            query_filter_source = data['query_filter_source']
        elif query_filter_source == "-":
            query_filter_source = "Enter Source Domain..."
        query_filter_target = request.form['filterinput-target']
        if query_filter_target == "":
            query_filter_target = data['query_filter_target']
        elif query_filter_target == "-":
            query_filter_target = "Enter Target Domain..."
        data={"query_search":query_search,"query_filter_artist":query_filter_artist,"query_filter_genre":query_filter_genre,"query_filter_songwriter":query_filter_songwriter,"query_filter_composer":query_filter_composer,"query_filter_source":query_filter_source,"query_filter_target":query_filter_target}
        write_data(data)
        cleared_results = get_results(data)
        metaphors = get_metaphors(cleared_results,query_filter_source,query_filter_target)
        
        return render_template('main.html',data=data,results=cleared_results,metaphors=metaphors)

    if request.method == 'GET':
        write_data({"query_search": "Enter your search query...", 
        "query_filter_artist": "Enter Artist Name...", 
        "query_filter_genre": "Enter Genre...",
        "query_filter_songwriter": "Enter Song Writer Name...",
        "query_filter_composer": "Enter Composer Name...",
        "query_filter_source": "Enter Source Domain...",
        "query_filter_target": "Enter Target Domain..."})
        return render_template('main.html', init='True')

def write_data(data):
    with open ('data.json','w') as f:
        f.write(json.dumps(data))

def get_data():
    with open('data.json') as f:
        data = json.loads(f.read())
        return data

def get_results(data):
    cleared_results_all = []
    if data['query_search'] != "Enter your search query...":
        basic_res = basic_search(data['query_search'])
        basic_results = basic_res['hits']['hits']
        cleared_basic_results = clear_results(basic_results)
        if len(cleared_basic_results) != 0:
            cleared_results_all.append(cleared_basic_results)
    if data['query_filter_artist'] != "Enter Artist Name...":
        artist_filter_res = artist_filter_search(data['query_filter_artist'])
        artist_filter_results = artist_filter_res['hits']['hits']
        cleared_artist_filter_results = clear_results(artist_filter_results)
        cleared_results_all.append(cleared_artist_filter_results)
    if data['query_filter_genre'] != "Enter Genre...":
        genre_filter_res = genre_filter_search(data['query_filter_genre'])
        genre_filter_results = genre_filter_res['hits']['hits']
        cleared_genre_filter_results = clear_results(genre_filter_results)
        cleared_results_all.append(cleared_genre_filter_results)
    if data['query_filter_songwriter'] != "Enter Song Writer Name...":
        songwriter_filter_res = songwriter_filter_search(data['query_filter_songwriter'])
        songwriter_filter_results = songwriter_filter_res['hits']['hits']
        cleared_songwriter_filter_results = clear_results(songwriter_filter_results)
        cleared_results_all.append(cleared_songwriter_filter_results)
    if data['query_filter_composer'] != "Enter Composer Name...":
        composer_filter_res = composer_filter_search(data['query_filter_composer'])
        composer_filter_results = composer_filter_res['hits']['hits']
        cleared_composer_filter_results = clear_results(composer_filter_results)
        cleared_results_all.append(cleared_composer_filter_results)
    if data['query_filter_source'] != "Enter Source Domain...":
        source_filter_res = source_filter_search(data['query_filter_source'])
        source_filter_results = source_filter_res['hits']['hits']
        cleared_source_filter_results = clear_results(source_filter_results)
        cleared_results_all.append(cleared_source_filter_results)
    if data['query_filter_target'] != "Enter Target Domain...":
        target_filter_res = target_filter_search(data['query_filter_target'])
        target_filter_results = target_filter_res['hits']['hits']
        cleared_target_filter_results = clear_results(target_filter_results)
        cleared_results_all.append(cleared_target_filter_results)
    if len(cleared_results_all) != 0:
        cleared_results = cleared_results_all[0]
        for list in cleared_results_all:
            if len(list) != 0:
                if len(cleared_results) >= len(list):
                    new_list = [dict for dict in cleared_results if dict in list]
                    cleared_results = new_list
                else:
                    new_list = [dict for dict in list if dict in cleared_results]
                    cleared_results = new_list
        return cleared_results


def clear_results(results):
    cleared_results=[]
    for result in results:
        cleared_results.append(result['_source'])
    return cleared_results

def get_metaphors(cleared_results,query_filter_source,query_filter_target):
    metaphors=[]
    if query_filter_source !="Enter Source Domain..." and query_filter_target !="Enter Target Domain...":
        for result in cleared_results:
            for metaphor in result['Metaphors']:
                source_domain = metaphor['Source Domain'] 
                target_domain = metaphor['Target Domain']
                if query_filter_source == source_domain or query_filter_source in source_domain.split() and target_domain == query_filter_target or query_filter_target in target_domain.split():
                    metaphors.append(metaphor)
    elif query_filter_source !="Enter Source Domain..." and query_filter_target =="Enter Target Domain...":
        for result in cleared_results:
            for metaphor in result['Metaphors']:
                source_domain = metaphor['Source Domain'] 
                if query_filter_source == source_domain or query_filter_source in source_domain.split():
                    metaphors.append(metaphor)
    elif query_filter_source =="Enter Source Domain..." and query_filter_target !="Enter Target Domain...":
        for result in cleared_results:
            for metaphor in result['Metaphors']:
                target_domain = metaphor['Target Domain']
                if target_domain == query_filter_target or query_filter_target in target_domain.split():
                    metaphors.append(metaphor)
    else:
        metaphors = None
    return metaphors

if __name__ == '__main__':
    app.run()



