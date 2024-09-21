import torch
from FM import FM
from DNN import DNN
import torch.nn as nn
import numpy
import torch.nn.functional as F


class DeepFM(nn.Module):
    def __init__(self, hidden, feature_col, dropout=0):
        super(DeepFM, self).__init__()
        # 连续型特征和离散型特征
        self.dense_col, self.sparse_col = feature_col
        self.embedding_layer = nn.ModuleDict({"embedding" + str(i): nn.Embedding(num_embeddings=feature["feature_num"],
                                                                                 embedding_dim=feature["embedding_dim"])
                                              for i, feature in enumerate(self.sparse_col)})

        self.feature_num = len(self.dense_col) + len(self.sparse_col) * self.sparse_col[0]["embedding_dim"]
        # 将feature_num插入到hidden的开头
        hidden.insert(0, self.feature_num)

        self.fm = FM(self.feature_num, self.sparse_col[0]["embedding_dim"])
        self.dnn = DNN(hidden, dropout)
        # 最终输出, 将最后一层输入然后输出一维的结果
        self.final = nn.Linear(hidden[-1], 1)

    def forward(self, x):
        sparse_input, dense_input = x[:, :len(self.sparse_col)], x[:, len(self.sparse_col):]
        sparse_input = sparse_input.long()
        sparse_embed = [self.embedding_layer["embedding" + str(i)](sparse_input[:, i]) for i in range(sparse_input.shape[1])]
        # 按照最后一个维度拼接
        sparse_embed = torch.cat(sparse_embed, dim=-1)

        x = torch.cat([sparse_embed, dense_input], dim=-1)
        wide_output = self.fm(x)
        deep_output = self.final(self.dnn(x))
        return F.sigmoid(torch.add(wide_output, deep_output)) * 5