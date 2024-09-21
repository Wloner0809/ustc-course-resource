import math
import json

path = ["./result_sota_beam20_batch1.json"]

result_dict = dict()
for p in path:
    result_dict[p] = {
        "NDCG": [],
        "HR": [],
    }

    f = open(p, "r")
    test_data = json.load(f)
    f.close()
    text = []
    for data in test_data:
        predict_list = data["predict"]
        predict_list = [_.strip('"') for _ in predict_list]
        text.append(predict_list)

    topk_list = [1, 3, 5, 10, 20]
    NDCG = []
    for topk in topk_list:
        S = 0
        for i in range(len(test_data)):
            target_item = test_data[i]["output"].strip('"')
            if target_item in text[i][:topk]:
                rankId = text[i].index(target_item)
                S = S + (1 / math.log(rankId + 2))
        NDCG.append(S / len(test_data) / (1 / math.log(2)))
    HR = []
    for topk in topk_list:
        S = 0
        for i in range(len(test_data)):
            target_item = test_data[i]["output"].strip('"')
            if target_item in text[i][:topk]:
                rankId = text[i].index(target_item)
                S = S + 1
        HR.append(S / len(test_data))
    print(NDCG)
    print(HR)
    print("_" * 100)
    result_dict[p]["NDCG"] = NDCG
    result_dict[p]["HR"] = HR

with open("./sota_beam20_batch1.json", "w") as f:
    json.dump(result_dict, f, indent=4)
