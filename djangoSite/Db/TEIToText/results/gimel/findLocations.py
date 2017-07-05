#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import collections
import pdb
from math import log
import unicodecsv as csv


class lex_value():
	def __init__(self, filename, list_of_words):
		self.filename = filename
		self.count_words = collections.Counter(list_of_words)
		self.len = len(list_of_words)

class tagged_word():
	def __init__(self, place, word, ner, ner_place, filename, name):
		self.place = place
		self.word = word
		self.ner = ner
		self.ner_place = ner_place
		self.filename = filename
		self.name = name

def find_name_of_lex_by_filename(filename):
	f = open('lexicon_txt/'+ filename, 'rb').readlines()
	return f[0][6:].replace('\n','')

def get_parsed_file_task2(artist, song):
	ret = []
	print artist + '/' + song
	f = open('tagged_songs' + '/' + artist + '/' + song, 'rb').read().split('\n\n')
	for p in f:
		r = p.split('\n')
		line_list = []
		for line in r:
			if len(line) > 3:
				place = line.split(' ')[0].replace('\t','').replace('null','').replace('\n','')
				word = line.split(' ')[1].replace('\t','').replace('null','').replace('\n','')
				ner = line.split(' ')[-1].replace('\t','').replace('null','').replace('\n','')
				if len(ner) > 1 and ner not in ['I_DATE']:
					line_list.append(tagged_word(place, word, ner[2:], ner[0], song, artist))
		line_list = merge_adjacents(line_list)
		ret = ret + line_list
	return ret

def merge_adjacents(line_list):
	ret = []
	if len(line_list) < 1:
		return []
	for i in range(len(line_list) - 1):
		if line_list[i].ner == line_list[i+1].ner and int(line_list[i].place) == (int(line_list[i+1].place) - 1) and line_list[i+1].ner_place == 'I':
			line_list[i+1].word = line_list[i].word + ' ' + line_list[i+1].word
		else:
			ret.append(line_list[i])
	ret.append(line_list[-1])
	return ret

def create_list_of_lex_values():
	ret = []
	files = os.listdir("parsed_lexicon")
	for x in files:
		ret.append(lex_value(x,get_parsed_file('parsed_lexicon/' + x)))
	return ret


#######main Task 2###############
test = []

os.chdir('tagged_songs')
subdirectories = [d for d in os.listdir('./') if os.path.isdir(os.path.join('./', d))]
os.chdir('..')
for artist in subdirectories:
	songs = os.listdir('tagged_songs' + '/' + artist)
	for song in songs:
		test = test + get_parsed_file_task2(artist, song)
	

with open('fix.tsv', 'a') as csv_file:
	csvfile = csv.writer(csv_file, encoding='utf-8', delimiter='\t')
	csvfile.writerow(['filename','name','ner','type'])
	for x in test:
		if x.ner in ['LOC']:
			print x.filename
			csvfile.writerow([x.filename,x.name,x.word,x.ner])


