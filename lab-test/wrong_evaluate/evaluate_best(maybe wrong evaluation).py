from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import math
import json
from tqdm import tqdm

path = ["./result_sota.json"]

"tokenizer and model"
tokenizer_path = "/data/terencewang/qwen"
base_model = "/data/terencewang/qwen"
tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
tokenizer.pad_token_id = 151644
tokenizer.padding_side = "left"
model = AutoModelForCausalLM.from_pretrained(
    base_model,
    torch_dtype=torch.bfloat16,
    device_map="auto",
)
model = model.to("cuda")
model.config.pad_token_id = 151644
model.eval()

"item id and item name mapping"
with open("../data/CD/item2id.txt", "r") as f:
    cd = f.readlines()
cd_names = [_.split("\t")[0] for _ in cd]
cd_ids = [int(_.split("\t")[1]) for _ in cd]
cd_dict = dict(zip(cd_names, cd_ids))

result_dict = dict()
for p in path:
    result_dict[p] = {
        "NDCG": [],
        "HR": [],
    }

    f = open(p, "r")
    test_data = json.load(f)
    f.close()
    text1 = [data["predict"][0].strip('"') for data in test_data]
    text2 = [data["predict"][1].strip('"') for data in test_data]
    text3 = [data["predict"][2].strip('"') for data in test_data]
    text4 = [data["predict"][3].strip('"') for data in test_data]

    def batch(list, batch_size=1):
        chunk_size = (len(list) - 1) // batch_size + 1
        for i in range(chunk_size):
            yield list[batch_size * i : batch_size * (i + 1)]

    predict_embeddings = []
    for i, batch_input in tqdm(enumerate(batch(text1, 16))):
        input = tokenizer(batch_input, return_tensors="pt", padding=True)
        input_ids = input.input_ids.to("cuda")
        attention_mask = input.attention_mask.to("cuda")
        outputs = model(
            input_ids, attention_mask=attention_mask, output_hidden_states=True
        )
        hidden_states = outputs.hidden_states
        predict_embeddings.append(hidden_states[-1][:, -1, :].detach())

    predict_embeddings = torch.cat(predict_embeddings, dim=0).cuda()
    item_embedding = torch.load("./data/cd/item_embedding_pad.pt").cuda()
    dist = torch.cdist(predict_embeddings, item_embedding, p=2)
    rank1 = dist
    rank1 = rank1.argsort(dim=-1).argsort(dim=-1)
    
    predict_embeddings = []
    for i, batch_input in tqdm(enumerate(batch(text2, 16))):
        input = tokenizer(batch_input, return_tensors="pt", padding=True)
        input_ids = input.input_ids.to("cuda")
        attention_mask = input.attention_mask.to("cuda")
        outputs = model(
            input_ids, attention_mask=attention_mask, output_hidden_states=True
        )
        hidden_states = outputs.hidden_states
        predict_embeddings.append(hidden_states[-1][:, -1, :].detach())

    predict_embeddings = torch.cat(predict_embeddings, dim=0).cuda()
    item_embedding = torch.load("./data/cd/item_embedding_pad.pt").cuda()
    dist = torch.cdist(predict_embeddings, item_embedding, p=2)
    rank2 = dist
    rank2 = rank2.argsort(dim=-1).argsort(dim=-1)
    
    predict_embeddings = []
    for i, batch_input in tqdm(enumerate(batch(text3, 16))):
        input = tokenizer(batch_input, return_tensors="pt", padding=True)
        input_ids = input.input_ids.to("cuda")
        attention_mask = input.attention_mask.to("cuda")
        outputs = model(
            input_ids, attention_mask=attention_mask, output_hidden_states=True
        )
        hidden_states = outputs.hidden_states
        predict_embeddings.append(hidden_states[-1][:, -1, :].detach())

    predict_embeddings = torch.cat(predict_embeddings, dim=0).cuda()
    item_embedding = torch.load("./data/cd/item_embedding_pad.pt").cuda()
    dist = torch.cdist(predict_embeddings, item_embedding, p=2)
    rank3 = dist
    rank3 = rank3.argsort(dim=-1).argsort(dim=-1)
    
    predict_embeddings = []
    for i, batch_input in tqdm(enumerate(batch(text4, 16))):
        input = tokenizer(batch_input, return_tensors="pt", padding=True)
        input_ids = input.input_ids.to("cuda")
        attention_mask = input.attention_mask.to("cuda")
        outputs = model(
            input_ids, attention_mask=attention_mask, output_hidden_states=True
        )
        hidden_states = outputs.hidden_states
        predict_embeddings.append(hidden_states[-1][:, -1, :].detach())

    predict_embeddings = torch.cat(predict_embeddings, dim=0).cuda()
    item_embedding = torch.load("./data/cd/item_embedding_pad.pt").cuda()
    dist = torch.cdist(predict_embeddings, item_embedding, p=2)
    rank4 = dist
    rank4 = rank4.argsort(dim=-1).argsort(dim=-1)

    topk_list = [1, 3, 5, 10, 20]
    NDCG = []
    for topk in topk_list:
        S = 0
        for i in range(len(test_data)):
            target_item = test_data[i]["output"].strip('"')
            target_item_id = cd_dict[target_item]
            rankId1 = rank1[i][target_item_id].item()
            rankId2 = rank2[i][target_item_id].item()
            rankId3 = rank3[i][target_item_id].item()
            rankId4 = rank4[i][target_item_id].item()
            if rankId1 < topk:
                S = S + (1 / math.log(rankId1 + 2))
            elif rankId2 < topk:
                S = S + (1 / math.log(rankId2 + 2))
            elif rankId3 < topk:
                S = S + (1 / math.log(rankId3 + 2))
            elif rankId4 < topk:
                S = S + (1 / math.log(rankId4 + 2))
        NDCG.append(S / len(test_data) / (1 / math.log(2)))
    HR = []
    for topk in topk_list:
        S = 0
        for i in range(len(test_data)):
            target_item = test_data[i]["output"].strip('"')
            target_item_id = cd_dict[target_item]
            rankId1 = rank1[i][target_item_id].item()
            rankId2 = rank2[i][target_item_id].item()
            rankId3 = rank3[i][target_item_id].item()
            rankId4 = rank4[i][target_item_id].item()
            if rankId1 < topk:
                S = S + 1
            elif rankId2 < topk:
                S = S + 1
            elif rankId3 < topk:
                S = S + 1
            elif rankId4 < topk:
                S = S + 1
        HR.append(S / len(test_data))
    print(NDCG)
    print(HR)
    print("_" * 100)
    result_dict[p]["NDCG"] = NDCG
    result_dict[p]["HR"] = HR

with open("./sota_best.json", "w") as f:
    json.dump(result_dict, f, indent=4)