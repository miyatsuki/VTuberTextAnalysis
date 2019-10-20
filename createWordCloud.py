import json
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from tqdm import tqdm, trange
import pathlib
import multiprocessing
import os
import time

channel_word_map = {}
with open("channel_word_map.tfidf.json", "r") as f:
    channel_word_map = json.load(f)

# 環境に合わせてフォントのパスを指定する。
# fpath = "/System/Library/Fonts/HelveticaNeue-UltraLight.otf"
fpath = "/Users/miyatsuki/Library/Fonts/NotoSansJP-Regular.otf"

unixtime = str(int(time.time()))
result_dir = 'results/' + unixtime
os.mkdir(result_dir)

def createWordCloud(path):
    word_weight_map = {}
    with open(path) as f:
        word_weight_map = json.load(f)

    if len(word_weight_map) > 0:
        wordcloud = WordCloud(
            background_color="white", font_path=fpath, width=900, height=500
        )
        wordcloud.generate_from_frequencies(word_weight_map)
        plt.figure(figsize=(15, 12))
        plt.imshow(wordcloud)
        plt.axis("off")

        channel_name = path.name.replace(".json", "")
        plt.savefig(result_dir + "/" + channel_name + ".png")
        plt.close()

def main():
    p = pathlib.Path('words_tfidf/')
    path_list = p.glob("*.json")

    print(multiprocessing.cpu_count())
    with multiprocessing.Pool(multiprocessing.cpu_count()) as p:
        p.map(createWordCloud, path_list)


if __name__ == "__main__":
    main()