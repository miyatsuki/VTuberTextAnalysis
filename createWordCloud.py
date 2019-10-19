import json
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from tqdm import tqdm, trange


channel_word_map = {}
with open("channel_word_map.tfidf.json", "r") as f:
    channel_word_map = json.load(f)

# 環境に合わせてフォントのパスを指定する。
# fpath = "/System/Library/Fonts/HelveticaNeue-UltraLight.otf"
fpath = "/Users/miyatsuki/Library/Fonts/NotoSansJP-Regular.otf"

num_lines = len(channel_word_map.keys())
with tqdm(total = num_lines) as pbar:
    for channel_name, value in channel_word_map.items():
        if len(value) > 0:
            #print(channel_name)
            #print(value)
            wordcloud = WordCloud(
                background_color="white", font_path=fpath, width=900, height=500
            )
            wordcloud.generate_from_frequencies(value)
            plt.figure(figsize=(15, 12))
            plt.imshow(wordcloud)
            plt.axis("off")
            # plt.show()

            plt.savefig("img/" + channel_name.replace("/", "_") + ".png")
            plt.close()
        pbar.update(1)
