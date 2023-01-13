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

* Unordered list can use asterisks
  

