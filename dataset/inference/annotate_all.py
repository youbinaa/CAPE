import pandas
import json
from tqdm import tqdm

sentenceTriple = dict()

def DNLI(data): #declaring dictionary with {sentence: [triples]} 
    global sentenceTriple 

    for pairs in data:
        if pairs["sentence1"] in sentenceTriple.keys():
            if pairs["triple1"] not in sentenceTriple[pairs["sentence1"]]:
                sentenceTriple[pairs["sentence1"]].append(pairs["triple1"])
        else: 
            sentenceTriple[pairs["sentence1"]] = [pairs["triple1"]]

        if pairs["sentence2"] in sentenceTriple.keys():
            if pairs["triple2"] not in sentenceTriple[pairs["sentence2"]]:
                sentenceTriple[pairs["sentence2"]].append(pairs["triple2"])
        else: 
            sentenceTriple[pairs["sentence2"]] = [pairs["triple2"]]


def convertToTriple(data):
    #{"source":"", "target_triple":[], "personas":[]}
    for dataset in tqdm(data):
        triplePersonas = []
        for per in dataset['personas']:
            if per in sentenceTriple.keys():
                triple = sentenceTriple[per]
                if triple != dataset["target_triple"]:
                    for _ in sentenceTriple[per]:
                        triplePersonas.append(_)
        dataset['personas_triple'] = triplePersonas

    with open("inference_dataset.json", "w") as file:
        json.dump(data, file) 

if __name__=="__main__":
    dataType = ["train", "dev", "test"]

    for t in dataType:
        #with open("dnli/dialogue_nli_extra/dialogue_nli_EXTRA_uu_{}.jsonl".format(t), "r", encoding = "utf-8") as json_file:
        with open("reference_dataset/dnli/dialogue_nli/dialogue_nli_{}.jsonl".format(t), "r", encoding = "utf-8") as json_file:
            data = json.load(json_file)
            DNLI(data)

    with open("dialogue_matched.json", "r", encoding = "utf-8") as json_file:
        data = json.load(json_file)
        convertToTriple(data)

