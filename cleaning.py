import json
import pathlib
from tqdm import tqdm, trange
import sys
import os
import re

path = pathlib.Path("video/")
json_list = list(path.glob("*.json"))

channel_sentence_map = {}

def replaceFullSpace(sentence):
    return sentence.replace('　', ' ').strip()


def hasURL(sentence):
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
    if channel not in channel_sentence_map:
        channel_sentence_map[channel] = []

    for raw_sentence in text.split("\n"):
        sentence = replaceFullSpace(raw_sentence.strip())
        if not hasURL(sentence) and len(sentence) > 0:
            channel_sentence_map[channel].append(sentence)

    return


for filePath in tqdm(json_list):
    with open(filePath, "r") as f:
        info = json.load(f)

        channelTitle = info["snippet"]["channelTitle"]
        title = info["snippet"]["title"]
        description = info["snippet"]["description"]

        addMap(channelTitle, title)
        addMap(channelTitle, description)


num_lines = sum(1 for line in open('tweets.json'))
with open('tweets.json', 'r') as f:
    with tqdm(total = num_lines) as pbar:
        for line in f:
            data = json.loads(line.strip())

            screen_name = data["screen_name"]
            text = data["text"]

            if screen_name not in channel_sentence_map:
                channel_sentence_map[channelTitle] = {}

            addMap(screen_name, text)
            pbar.update(1)


for channelTitle in channel_sentence_map:
    filename = channelTitle.replace("/", "_")

    with open("sentences/" + filename + ".json", "w") as f:
        json.dump(channel_sentence_map[channelTitle], f, ensure_ascii=False, indent=2)