import json
import pandas as pd
from tqdm import tqdm

df = pd.DataFrame({})

def PersonaChat():
    global df
    
    json_file = open("reference_dataset/personachat_self_original_deleted.json", "r", encoding = "utf-8")
    data = json.load(json_file)
    trainData = data["train"]
    validData = data["valid"]

    df1 = pd.DataFrame(trainData)
    df2 = pd.DataFrame(validData)

    df = pd.concat([df1, df2], ignore_index=True)
    split_per = pd.DataFrame(df['personality'].tolist(), columns = ['persona1', 'persona2', 'persona3', 'persona4', 'persona5'])
    df = pd.concat([df, split_per], axis=1)
    #df = df.drop(columns = ['personality'])

    split_utt = pd.DataFrame(df['utterances'].tolist())
    df = pd.concat([df, split_utt], axis=1)
    df = df.drop(columns = ['utterances'])

def findPCDialogue(tripleData):
    result = []
    #output = {"source":"", "target_triple":[], "personas":[]}

    col = ['persona1', 'persona2', 'persona3', 'persona4', 'persona5']
    
    #df.columns = personality / persona1 - persona5 / 0 - 24

    for sentence in tqdm(tripleData):
        result_index = []
        for per in col:
            index = df[df[per]==sentence].index
            result_index.append(index)
        for i in range(25):
            index = df[df[i]==sentence].index
            result_index.append(index)

        #all indexes that the sentence in dnli belongs to 
        res = set().union(*result_index) 
        temp = []
        for possible in res:
            personaSet = set(df.iloc[possible]['personality'])
            if personaSet not in temp:
                temp.append(personaSet)
                output = {"source":"", "target_triple":[], "personas":[]}
                output["source"]=sentence
                output["target_triple"]=tripleData[sentence]
                output["personas"]=df.iloc[possible]['personality']
                result.append(output)
    
    with open("dialogue_matched.json", "w") as file:
        json.dump(result, file)

if __name__=="__main__":
    PersonaChat()
    
    with open("non_dropped_triples.json", "r", encoding = "utf-8") as json_file:
        data = json.load(json_file)
        findPCDialogue(data)

