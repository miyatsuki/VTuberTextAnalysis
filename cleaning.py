import json
import pathlib
from tqdm import tqdm, trange
import sys
import os
import re

path = pathlib.Path("sources/video/")
json_list = list(path.glob("*.json"))

raw_channel_sentence_map = {}

def replaceFullSpace(sentence):
    return sentence.replace('　', ' ').strip()


def hasInvalidText(sentence):
    # 基本形
    if "http" in sentence:
        return True

    # co.jp
    if ".co.jp" in sentence:
        return True

    # com
    if ".com" in sentence:
        return True

    # 部分一致
    # "souyaichika.info@gmail.co…" とか
    if "gmail." in sentence:
        return True
    

    # ©は除外
    # TODO: url関係ないのでどうにかする
    if "©" in sentence:
        return True

    # RTは除外
    if sentence.startswith("RT "):
        return True

    return False


def addMap(channel, text):
    channel = channel.replace("/", "_")
    if channel not in raw_channel_sentence_map:
        raw_channel_sentence_map[channel] = []

    for raw_sentence in text.split("\n"):
        sentence = replaceFullSpace(raw_sentence.strip())
        if not hasInvalidText(sentence) and len(sentence) > 0:
            raw_channel_sentence_map[channel].append(sentence)

    return


for filePath in tqdm(json_list):
    with open(filePath, "r") as f:
        info = json.load(f)

        channelTitle = info["snippet"]["channelTitle"]
        title = info["snippet"]["title"]
        description = info["snippet"]["description"]

        addMap(channelTitle, title)
        addMap(channelTitle, description)


num_lines = sum(1 for line in open('sources/tweets.json'))
with open('sources/tweets.json', 'r') as f:
    with tqdm(total = num_lines) as pbar:
        for line in f:
            data = json.loads(line.strip())

            screen_name = data["screen_name"]
            text = data["text"]

            if screen_name not in raw_channel_sentence_map:
                raw_channel_sentence_map[channelTitle] = {}

            addMap(screen_name, text)
            pbar.update(1)

nayose_map = {}
with open("nayose.tsv") as f:
    for line in f:
        before = line.strip().split("\t")[0]
        after = line.strip().split("\t")[1]
        nayose_map[before] = after

channel_sentence_map = {}
for raw_channelTitle in raw_channel_sentence_map:
    sentences = raw_channel_sentence_map[raw_channelTitle]

    if raw_channelTitle not in nayose_map:
        print(raw_channelTitle)
        continue

    channelTitle = nayose_map[raw_channelTitle]

    if channelTitle not in channel_sentence_map:
        channel_sentence_map[channelTitle] = []

    channel_sentence_map[channelTitle] += sentences

# save
for channelTitle in channel_sentence_map:
    with open('sentences/' + channelTitle + ".json", 'w') as f:
        json.dump(channel_sentence_map[channelTitle], f, ensure_ascii=False, indent=2)