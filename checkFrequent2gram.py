import json

gram_map = {}
for t in ["gram2", "gram3", "gram4"]:
    print("===" + t + "===")
    with open(t + "_map.json", "r") as f:
        gram_map = json.load(f)

    for gram, freq in gram_map.items():
        if freq >= 10000:
            print("\t".join([gram, str(freq)]))
