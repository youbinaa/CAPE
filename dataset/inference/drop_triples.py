import pandas as pd
import json
from ftfy import fix_text
import operator
#{"label": "positive", 
#"sentence1": "yeah dogs scare me . i prefer horses too .", 
#"sentence2": "what about pets ? i am terrified of dogs but bet your kids love them ?", 
#"triple1": ["i", "dislike", "dog"], 
#"triple2": ["i", "dislike", "dog"], 
#"dtype": "matchingtriple_uu", 
#"id": "dialogue_nli_EXTRA_uu_test_8696"}

sentenceTriple = dict()

def dataStatistics(): #checking data statistics of sentence-triples dictionary 
    hSet = dict()
    
    for sentence in sentenceTriple.keys():
        for triple in sentenceTriple[sentence]:
            h, r, t = triple[0], triple[1], triple[2]
            if h in hSet.keys():
                hSet[h]+=1
            else:
                hSet[h]=1
    sorted_d = dict( sorted(hSet.items(), key=operator.itemgetter(1),reverse=True))
    print(sorted_d)
    return

def dropData():
    dropItems = {"<blank>", "<none>", "other"}
    leaveHead = {"i", "my", "me"}
    for sentence in sentenceTriple.keys():
        for triple in sentenceTriple[sentence][:]:
            h, r, t = triple[0], triple[1], triple[2]
            if r in dropItems or t in dropItems or h not in leaveHead:
                sentenceTriple[sentence].remove(triple)
    
    for sentence in list(sentenceTriple):
        if len(sentenceTriple[sentence])==0:
            del sentenceTriple[sentence]

def dumpData():
    with open("non_dropped_triples.json", "w") as file:
        json.dump(sentenceTriple, file)

def createDataset(data): #declaring dictionary with {sentence: [triples]} 
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

if __name__ == "__main__":
    dataType = ["train", "dev", "test"]

    for t in dataType:
        #with open("dnli/dialogue_nli_extra/dialogue_nli_EXTRA_uu_{}.jsonl".format(t), "r", encoding = "utf-8") as json_file:
        with open("reference_dataset/dnli/dialogue_nli/dialogue_nli_{}.jsonl".format(t), "r", encoding = "utf-8") as json_file:
            data = json.load(json_file)
            createDataset(data)
    #dataStatistics()
    dropData()
    dumpData()
