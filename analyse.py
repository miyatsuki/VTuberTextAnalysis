from janome.tokenizer import Tokenizer
import json
import pathlib
from tqdm import tqdm, trange
import sys
import multiprocessing
from collections import namedtuple

# gram2_map = {}
# gram3_map = {}
# gram4_map = {}
# channel_word_map = {}

path = pathlib.Path("video/")
json_list = list(path.glob("*.json"))

def getWords(tokenizer, text):
    ans = []
    for token in t.tokenize(text):
        baseForm = token.base_form
        pos = token.part_of_speech.split(",")
        if (
            pos[0] == "名詞"
            and pos[1] == "一般"
        ) or pos[0] == "カスタム名詞":
            ans.append(baseForm)

    return ans


def getTokens(Tokenizer, text):
    ans = []
    for token in t.tokenize(text, wakati=True):
        ans.append(token)
    return ans


def getNgrams(textArray, N):
    ans = []
    for i in range(len(textArray) - (N - 1)):
        ans.append("".join(textArray[i : i + N]))
    return ans

t = Tokenizer("simpledic.csv", udic_type="simpledic", udic_enc="utf8")
def createMapFile(path):
    ans = {}

    sentences = []
    with open(path) as f:
        sentences = json.load(f) 

    for text in sentences:
        words = getWords(t, text)
        for word in words:
            if word not in ans:
                ans[word] = 0

            ans[word] += 1

    with open("words/" + path.name, "w") as f:
        json.dump(ans, f, ensure_ascii=False, indent=2)

    """
    token_list = getTokens(tokenizer, text)
    
    gram2_list = getNgrams(token_list, 2)
    for gram in gram2_list:
        if gram not in gram2_map:
            gram2_map[gram] = 0
        gram2_map[gram] += 1

    gram3_list = getNgrams(token_list, 3)
    for gram in gram3_list:
        if gram not in gram3_map:
            gram3_map[gram] = 0
        gram3_map[gram] += 1

    gram4_list = getNgrams(token_list, 4)
    for gram in gram4_list:
        if gram not in gram4_map:
            gram4_map[gram] = 0
        gram4_map[gram] += 1
    """

#with open("gram2_map.json", "w") as f:
#    json.dump(gram2_map, f, ensure_ascii=False)

#with open("gram3_map.json", "w") as f:
#    json.dump(gram3_map, f, ensure_ascii=False)

#with open("gram4_map.json", "w") as f:
#    json.dump(gram4_map, f, ensure_ascii=False)


def main():
    p = pathlib.Path('sentences/')
    path_list = p.glob("*.json")

    print(multiprocessing.cpu_count())
    with multiprocessing.Pool(multiprocessing.cpu_count()) as p:
        p.map(createMapFile, path_list)


if __name__ == "__main__":
    main()