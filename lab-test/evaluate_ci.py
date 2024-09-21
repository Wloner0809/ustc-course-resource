from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import math
import json
from tqdm import tqdm

path = ["result_sota.json"]

"tokenizer and model"
tokenizer_path = "/data/terencewang/qwen"
base_model = "/data/terencewang/qwen"
tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
# tokenizer.pad_token_id = 0
tokenizer.pad_token_id = 151644
tokenizer.padding_side = "left"
model = AutoModelForCausalLM.from_pretrained(
    base_model,
    torch_dtype=torch.bfloat16,
    device_map="auto",
)
model = model.to("cuda")
# model.config.pad_token_id = 0
model.config.pad_token_id = 151644
model.eval()

"item id and item name mapping"
with open("../data/CD/item2id.txt", "r") as f:
    cd = f.readlines()
cd_names = [_.split("\t")[0] for _ in cd]
cd_ids = [int(_.split("\t")[1]) for _ in cd]
cd_dict = dict(zip(cd_names, cd_ids))

topk_list = [1, 3, 5, 10, 20]
result_dict = dict()


def get_dist(test_data):
    f.close()
    text = []
    for data in test_data:
        if data["predict"][0].strip('"') != "":
            text.append(data["predict"][0].strip('"'))
        elif data["predict"][1].strip('"') != "":
            text.append(data["predict"][1].strip('"'))
        elif data["predict"][2].strip('"') != "":
            text.append(data["predict"][2].strip('"'))
        elif data["predict"][3].strip('"') != "":
            text.append(data["predict"][3].strip('"'))
        else:
            text.append("None")

    def batch(list, batch_size=1):
        chunk_size = (len(list) - 1) // batch_size + 1
        for i in range(chunk_size):
            yield list[batch_size * i : batch_size * (i + 1)]

    predict_embeddings = []
    for i, batch_input in tqdm(enumerate(batch(text, 1))):
        input = tokenizer(batch_input, return_tensors="pt", padding=True)
        input_ids = input.input_ids.to("cuda")
        attention_mask = input.attention_mask.to("cuda")
        outputs = model(
            input_ids, attention_mask=attention_mask, output_hidden_states=True
        )
        hidden_states = outputs.hidden_states
        predict_embeddings.append(hidden_states[-1][:, -1, :].detach())

    predict_embeddings = torch.cat(predict_embeddings, dim=0).cuda()
    # item_embedding = torch.load("./data/cd/item_embedding.pt").cuda()
    item_embedding = torch.load("./data/cd/item_embedding_pad.pt").cuda()
    dist = torch.cdist(predict_embeddings, item_embedding, p=2)
    dist_min = torch.min(dist, dim=1, keepdim=True)[0]
    dist_max = torch.max(dist, dim=1, keepdim=True)[0]
    dist_norm = (dist - dist_min) / (dist_max - dist_min)
    return dist_norm


def get_ndcg(test_data, rank):
    NDCG = []
    for topk in topk_list:
        S = 0
        for i in range(len(test_data)):
            target_item = test_data[i]["output"].strip('"')
            target_item_id = cd_dict[target_item]
            rankId = rank[i][target_item_id].item()
            if rankId < topk:
                S = S + (1 / math.log(rankId + 2))
        NDCG.append(S / len(test_data) / (1 / math.log(2)))
    return NDCG


def get_hr(test_data, rank):
    HR = []
    for topk in topk_list:
        S = 0
        for i in range(len(test_data)):
            target_item = test_data[i]["output"].strip('"')
            target_item_id = cd_dict[target_item]
            rankId = rank[i][target_item_id].item()
            if rankId < topk:
                S = S + 1
        HR.append(S / len(test_data))
    return HR


for p in path:
    result_dict[p] = {
        "NDCG": [],
        "HR": [],
    }
    f = open(p, "r")
    test_data = json.load(f)
    dist = get_dist(test_data)
    ci_rank = torch.load("../SASRec.pytorch/val.pt")
    assert ci_rank.shape == dist.shape
    ci_min = torch.min(ci_rank, dim=1, keepdim=True)[0]
    ci_max = torch.max(ci_rank, dim=1, keepdim=True)[0]
    ci_norm = (ci_rank - ci_min) / (ci_max - ci_min)
    ci_rank = ci_norm
    max_ndcg = [0 for _ in range(5)]
    max_hr = [0 for _ in range(5)]
    max_gamma_ndcg = [-1 for _ in range(5)]
    max_gamma_hr = [-1 for _ in range(5)]

    g_list = (
        [-i for i in range(1, 100)]
        + [i / 100 for i in range(100)]
        + [i for i in range(1, 100)]
    )
    # g_list = (
    #     [i / 100 for i in range(100)]
    #     + [1 + i / 100 for i in range(100)]
    #     + [2 + i / 100 for i in range(100)]
    #     + [3 + i / 100 for i in range(100)]
    # )
    for g in tqdm(g_list):
        gamma = g
        rank = torch.pow((1 + ci_rank), -gamma) * dist
        rank = rank.argsort(dim=-1).argsort(dim=-1)
        NDCG = get_ndcg(test_data, rank)
        HR = get_hr(test_data, rank)
        for i in range(5):
            if NDCG[i] > max_ndcg[i]:
                max_ndcg[i] = NDCG[i]
                max_gamma_ndcg[i] = gamma
            if HR[i] > max_hr[i]:
                max_hr[i] = HR[i]
                max_gamma_hr[i] = gamma

    print("max_gamma_ndcg:", max_gamma_ndcg)
    print("max_gamma_hr:", max_gamma_hr)

    f = open(p, "r")
    test_data = json.load(f)
    dist = get_dist(test_data)
    ci_rank = torch.load("../SASRec.pytorch/test.pt")
    assert ci_rank.shape == dist.shape
    ci_min = torch.min(ci_rank, dim=1, keepdim=True)[0]
    ci_max = torch.max(ci_rank, dim=1, keepdim=True)[0]
    ci_norm = (ci_rank - ci_min) / (ci_max - ci_min)
    ci_rank = ci_norm

    Best_NDCG = []
    Best_HR = []
    for i in range(5):
        gamma = max_gamma_ndcg[i]
        rank = torch.pow((1 + ci_rank), -gamma) * dist
        rank = rank.argsort(dim=-1).argsort(dim=-1)
        NDCG = get_ndcg(test_data, rank)
        Best_NDCG.append(NDCG[i])
        gamma = max_gamma_hr[i]
        rank = torch.pow((1 + ci_rank), -gamma) * dist
        rank = rank.argsort(dim=-1).argsort(dim=-1)
        HR = get_hr(test_data, rank)
        Best_HR.append(HR[i])
    result_dict[p]["NDCG"] = Best_NDCG
    result_dict[p]["HR"] = Best_HR
    print(Best_NDCG)
    print(Best_HR)


f = open("./sota_ci.json", "w")
json.dump(result_dict, f, indent=4)
f.close()
