import requests
from bs4 import BeautifulSoup
import csv
from googletrans import Translator
import json,re

def create_songs_links_list():
    with open("./data/songs_links.csv", 'r') as file:
        links_list = []
        count=0
        csvreader = csv.reader(file)
        for link in csvreader:
            if count<=149:
                    links_list.append(link[0])
                    count+=1
        return links_list

def create_metaphor_data_list():
    with open("./data/metaphors.csv", 'r', encoding="utf8") as file:
        all_songs_metaphor_list = []
        csvreader = csv.reader(file)
        for data in csvreader:
                all_songs_metaphor_list.append(data)
        return all_songs_metaphor_list

def get_methaphor_data(count,count_last,all_songs_metaphor_list):
        metaphor_data_list = []
        for count_m in range(count_last,len(all_songs_metaphor_list)):
                if all_songs_metaphor_list[count_m][0]==str(count) or all_songs_metaphor_list[count_m][0]=="":
                        metaphor_data = {}
                        for count_md in range(1,len(all_songs_metaphor_list[count_m])):
                                metaphor_data[all_songs_metaphor_list[0][count_md]]=all_songs_metaphor_list[count_m][count_md]
                        metaphor_data_list.append(metaphor_data)
                else:
                        count_last = count_m
                        return metaphor_data_list,count_last
        return metaphor_data_list,count_last

def scrape_pages(url_list,all_metaphor_list,count_last):
        meta_data_list = []
        url_list=url_list[:10]
        for count in range(len(url_list)):
                url = url_list[count]
                headers = requests.utils.default_headers()
                res = requests.get(url, headers)
                meta_data,count_last = get_song_info(res.content,count,all_metaphor_list,count_last)
                meta_data_list.append(meta_data)
        write_data(meta_data_list)

def translate_meta_data(key,vals):
	if key != "Title" and key != "Lyrics":
		key = translate_to_sinhala(key)
		if isinstance(vals, list):
			value = []
			for phrase in vals :
				value.append(translate_to_sinhala(phrase))
		else:
			value = translate_to_sinhala(vals)
	return value

def translate_to_sinhala(value):
	translator = Translator()
	sinhala_val = translator.translate(value, dest='si')
	return sinhala_val.text

def get_song_info(song_page,count,all_metaphor_list,count_last):
	print("Getting song info :",count+1)
	song_meta_data = {}
	song_meta_data['Song ID'] = count+1
	soup = BeautifulSoup(song_page, 'html.parser')
	song = soup.find('h1', {'class': 'entry-title'})
	artist = soup.find('span', {'class': 'entry-categories'})
	genre = soup.find('span', {'class': 'entry-tags'})
	songwriter = soup.find('span', {'class': 'lyrics'})
	music = soup.find('span', {'class': 'music'})
	movie = soup.find('span', {'class': 'movies'})
	lyrics = parse_lyrics(soup.find_all('pre')[0].get_text())
	if song : 
		song_meta_data['Title'] = song.get_text()
	song_list = [artist, genre, songwriter, music]
	for key_val in song_list:
		if key_val :
			if isinstance(key_val, str):
				key_vals = key_val_split(key_val)
			else :
				key_vals = key_val_split(key_val.get_text())
			if key_vals :
				key = key_vals[0]
				if (key=='Tags'):
					key = "Genre"
				if (key=='Lyrics'):
					key = "Song Writer"
				vals = key_vals[1]
				song_meta_data['{}_en'.format(key)] = vals
				if (vals!='Unknown'):
					song_meta_data['{}_si'.format(key)] = translate_meta_data(key,vals)
	if genre:
                if ("Movie Songs" in song_meta_data['Genre_en']):
                        if movie:
                                key_vals = key_val_split(movie.get_text())
                                key = key_vals[0]
                                vals = key_vals[1]
                                song_meta_data['{}_en'.format(key)] = vals
                                if (vals!='Unknown'):
                                        song_meta_data['{}_si'.format(key)] = translate_meta_data(key,vals)
	if lyrics :
		song_meta_data['Lyrics'] = lyrics
	song_meta_data['Metaphors'],count_last = get_methaphor_data(count+1,count_last,all_metaphor_list)
	return song_meta_data,count_last

def write_data(data):
	with open ('./data/songs_dataset.json','a') as f:
		f.write(json.dumps(data))

def key_val_split(key_val):
	key_val_list = key_val.split(":")
	if len(key_val_list) >= 2 :
		key = key_val_list[0]
		vals = key_val_list[1]
		if vals[0] == " ":
			vals = vals[1:]
		if "," in vals :
			vals = vals.split(", ")
		return key, vals

def parse_lyrics(lyrics):
	space_set = set([' '])
	processed = ''
	regex = r"([A-z])+|[0-9]|\||-|∆|([.!?\\\/\(\)\+#&])+"
	lyric_lines = lyrics.split('\n')
	for line in lyric_lines:
		new = re.sub(regex, '', line)
		chars = set(new)
		if not ((chars == space_set) or (len(chars) is 0)):
			processed += new + '\n'
	return processed

def create_meta_all():
	dict_all_meta = {}
	list_keys = ['Artist_en', 'Artist_si', 'Genre_en', 'Genre_si', 'Song Writer_en', 'Song Writer_si', 'Music_en', 'Music_si', 'Lyrics', 'Metaphors']
	for i in list_keys :
		dict_all_meta[i] = []

	with open('./data/songs_dataset.json') as f:
		data = json.loads(f.read())

	for items in data:
		for key in items:
			if key in list_keys:
				if type(items[key]) == list:
					for val in items[key]:
						if val not in dict_all_meta[key]:
							dict_all_meta[key].append(val)
				else :
					if items[key] not in dict_all_meta[key]:
						dict_all_meta[key].append(items[key])
	
	with open ('./templates/data/songs_meta_all.json','w+') as f:
		f.write(json.dumps(dict_all_meta))

if __name__ == "__main__":
        all_metaphor_list = create_metaphor_data_list()
        count_last = 1
        scrape_pages(create_songs_links_list(),all_metaphor_list,count_last)
        create_meta_all()

	
        
