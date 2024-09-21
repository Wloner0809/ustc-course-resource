import pandas as pd
from tqdm import tqdm
from transformers import BertTokenizer, BertModel
import torch

# # 将tag信息提取为Embedding
# tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
# model = BertModel.from_pretrained('bert-base-chinese').cuda()
# # 读loaded_data取保存的 CSV 文件
# loaded_data = pd.read_csv('../Dataset/selected_book_top_1200_data_tag.csv')
# tag_embedding_dict = {}

# with torch.no_grad():
#     for index, rows in tqdm(loaded_data.iterrows()):
#         # 将标签列表转换为字符串
#         tags_str = " ".join(rows.Tags)
#         # 使用BERT中文模型对标签进行编码
#         inputs = tokenizer(tags_str, truncation=True, return_tensors='pt')
#         outputs = model(inputs.input_ids.cuda(), inputs.token_type_ids.cuda(), inputs.attention_mask.cuda())
#         # 使用最后一层的平均隐藏状态作为标签的向量表示
#         tag_embedding = outputs.last_hidden_state.mean(dim=1).cpu()
#         tag_embedding_dict[rows.Book] = tag_embedding
#
# tag_embedding = []
# for id_ in loaded_data["Book"]:
#     tag_embedding.append(tag_embedding_dict[id_])
# tag_info = pd.DataFrame({"Tag": tag_embedding})

# 读取Movie_info中的信息
movie_info_json = pd.read_json('../../Stage1_1/Result/Movie_info.json')
movie_info_json.to_csv('../Dataset/movie_info.csv', index=False)
movie_info = pd.read_csv('../Dataset/movie_info.csv')

# 读取book_score中的信息
movie_score = pd.read_csv('../Dataset/movie_score.csv')
# 将Time进行离散化分桶处理
# 按天数进行离散化
movie_score["Time"] = pd.to_datetime(movie_score["Time"]).dt.day
# 制作DataFrame
favor, watched = [], []
for id_ in movie_score["Movie"]:
    if str(id_) in movie_info.columns:
        favor.append(movie_info[str(id_)].iloc[1])
        watched.append(movie_info[str(id_)].iloc[2])
new_info = pd.DataFrame({"favor": favor, "watched": watched})
# 添加爬虫信息后的DataFrame
final_info = pd.concat([movie_score, new_info], axis=1)
del final_info["Tag"]
# 写入文件
final_info.to_csv("../Dataset/movie_final_info.csv", index=False)
