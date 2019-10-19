from tqdm import tqdm, trange
import sys
import json
import math

channel_word_map = {}
with open('channel_word_map.json', 'r') as f:
    channel_word_map = json.load(f)

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

with open('channel_word_map.tfidf.json', 'w') as f:
    json.dump(channel_word_tfidf_map, f, ensure_ascii=False)