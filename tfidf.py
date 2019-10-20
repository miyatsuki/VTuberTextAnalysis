from tqdm import tqdm, trange
import sys
import json
import math
import pathlib

p = pathlib.Path('words/')
path_list = p.glob("*.json")

channel_word_map = {}
for path in path_list:
    with open(path, 'r') as f:
        channel_name = path.name.replace(".json", "")
        channel_word_map[channel_name] = json.load(f)

channel_freq_map = {}
word_appear_map = {}

print("count words")
for channel in tqdm(channel_word_map.keys()):
    channel_freq_map[channel] = 0
    for word in channel_word_map[channel]:
        if word not in word_appear_map:
            word_appear_map[word] = 0
        
        word_appear_map[word] += 1
        channel_freq_map[channel] += channel_word_map[channel][word]

print("calc tf-idf")
channel_word_tfidf_map = {}
for channel in tqdm(channel_word_map.keys()):
    channel_word_tfidf_map[channel] = {}
    for word in channel_word_map[channel]:
        tf = channel_word_map[channel][word] / channel_freq_map[channel]
        idf = math.log(len(channel_word_map.keys())/word_appear_map[word])
        channel_word_tfidf_map[channel][word] = tf * idf

for channel_name in channel_word_tfidf_map:
    with open('words_tfidf/' + channel_name + '.json', 'w') as f:
        json.dump(channel_word_tfidf_map[channel_name], f, ensure_ascii=False, indent=2)