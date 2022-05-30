import json

def filterOut(data):
    dataType = ["train", "valid"]
    
    for t in dataType:
        for j in range(len(data[t])):
            i = data[t][j]
            history = i["utterances"][-1]["history"]
            response = i["utterances"][-1]["candidates"][-1]
            history.append(response)
            history = history[1::2]
            i["utterances"]=history

    with open("personachat_self_original_deleted.json", "w", encoding = "utf-8") as json_file:
        json.dump(data, json_file)

    return

if __name__=="__main__":
    with open("personachat_self_original.json", "r", encoding = "utf-8") as json_file:
        data = json.load(json_file)
        filterOut(data)