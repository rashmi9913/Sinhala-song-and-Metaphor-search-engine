# Sinhala Song and Metaphor Search Engine

This repository contains source code for Sinhala song and metaphor search engine done for module CS4642 - Data Mining & Information Retrieval.

## Introduction

A search engine developed using Python and Elasticsearch that can be used to search Sinhala songs that include metaphors. The search engine contains data of 150 Sinhala songs including metaphors,their interpretations,source domains and target domains. The songs data were scraped from [Sinhala Songbook](https://www.sinhalasongbook.com/).

## Main functions of the system

1. Searching songs that include metaphors using the Title, Lyric, Metaphor and Metaphor interpretation.
2. Faceted search.
   - Users will be able to filter search results based on the Artist, Genre, Songwriter, Composer, Metaphor source domain and Metaphor target domain.
   - Multi filtering is also supported.
3. Recommending metaphors based on the source domain and target domain of metaphors.
4. Bilingual Support.
   - Searching songs using the Title of the song in both Sinhala and English search terms are supported by the search engine.
5. Synonyms Support.
   - The search engine supports synonyms.

## Directory structure

```
├── data : Data scraped from [Sinhala Songbook](https://www.sinhalasongbook.com/)                    
    ├── songs_dataset.json : Contains original data of all songs scraped form the website
    ├── metaphors.csv : Contains metaphor, interpretaion, source domain and target domain related to metaphors in each song
    └── songs_links.csv : Contains links of all songs 
├── templates : UI related files                   
    ├── css 
	└── main.css : Contains stylings of the main page
    ├── data  
	└── songs_meta_all.json : Contains all meta date related to the songs
    └── main.html : html code for the main page  
├── app.py : Backend of the web app created using Flask 
├── data.json : Contains data that are related to previous sarch
├── insertToElasticSearch.py : File to upload data and mappings to elasticsearch cluster by creating an index
├── query.py :  Elasticsearch queries  
├── scraper.py :  Source code for the data scraper  
└── search.py : Search functions used to classify user search phrases  
```

## Details about the dataset

Each song contains following data fields.

* Song ID 
* Title : Title of the song (both in Sinhala and English)
* Artist_en : Artist/List of artists of the song  in English
* Artist_si : Artist/List of artists of the song  in Sinhala
* Genre_en : Genre/List of genres of the song in English
* Genre_si : Genre/List of genres of the song in Sinhala
* Song Writer_en : Song writer/List of song writers of the song in English
* Song Writer_si : Song writer/List of song writers of the song in Sinhala
* Music_en : Composer/List of composers of the song in English
* Music_si : Composer/List of composers of the song in English
* Lyrics : Lyrics of the song
* Metaphors : Metaphor/List of metaphors in the song
   - Metaphor
   - Interpretation
   - Source Domain
   - Target Domain

## Starting the web app

### Pre requesists :
   - Python, Elasticsearch and Kibana needed in your PC
   
### Getting started with the web app :
   - Start elasticsearch cluster on port 9200 run Kibana
   - Clone the repository
   ```
   https://github.com/rashmi9913/Sinhala-song-and-Metaphor-search-engine.git
   ```
   - Create Python vurtual environment
   ```
   cd ...
   pip install virtualenv
   virtualenv <!--env_name-->
   <!--env_name-->\Scripts\activate
   ```
   - Install required libraries
   ```
   pip3 install requests
   pip3 install beautifulsoup4
   pip3 install googletrans==4.0.0rc1
   pip3 install elasticsearch 
   pip3 install elasticsearch-dsl
   ```
   - Run scraper.py to scrape data from the website
   ```
   py scraper.py
   ```
   - Run insertToElasticSearch.py to insert the corpus and mappings to the Elasticsearch by create the index 
   ```
   py insertToElasticSearch.py
   ```
   - Start search engine app by running app.py
   ```
   Flask --app app run
   ```

