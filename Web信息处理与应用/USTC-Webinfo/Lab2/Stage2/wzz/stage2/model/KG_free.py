import torch
from torch import nn
from torch.nn import functional as F


def _L2_loss_mean(x):
    return torch.mean(torch.sum(torch.pow(x, 2), dim=1, keepdim=False) / 2.)


class KG_free(nn.Module):

    def __init__(self, args, n_users, n_items):

        super(KG_free, self).__init__()

        self.n_users = n_users
        self.n_items = n_items
        self.embed_dim = args.embed_dim
        self.l2loss_lambda = args.l2loss_lambda

        self.user_embed = nn.Embedding(self.n_users, self.embed_dim)
        self.item_embed = nn.Embedding(self.n_items, self.embed_dim)

        # 初始化神经网络的参数
        # 根据输入和输出的维度来初始化权重矩阵，确保每个神经元在前向传播时输出具有相似方差
        # 防止在反向传播过程中梯度消失/梯度爆炸
        nn.init.xavier_uniform_(self.user_embed.weight)
        nn.init.xavier_uniform_(self.item_embed.weight)


    def calc_score(self, user_ids, item_ids):
        """
        user_ids:   (n_users)
        item_ids:   (n_items)
        """
        user_embed = self.user_embed(user_ids)                              # (n_users, embed_dim)
        item_embed = self.item_embed(item_ids)                              # (n_items, embed_dim)
        # 计算矩阵P和矩阵Q的内积
        cf_score = torch.matmul(user_embed, item_embed.transpose(0, 1))     # (n_users, n_items)
        return cf_score


    def calc_loss(self, user_ids, item_pos_ids, item_neg_ids):
        """
        user_ids:       (batch_size)
        item_pos_ids:   (batch_size)
        item_neg_ids:   (batch_size)
        """
        user_embed = self.user_embed(user_ids)                              # (batch_size, embed_dim)
        item_pos_embed = self.item_embed(item_pos_ids)                      # (batch_size, embed_dim)
        item_neg_embed = self.item_embed(item_neg_ids)                      # (batch_size, embed_dim)

        pos_score = torch.sum(user_embed * item_pos_embed, dim=1)           # (batch_size)
        neg_score = torch.sum(user_embed * item_neg_embed, dim=1)           # (batch_size)

        # BPR Loss
        cf_loss = (-1.0) * F.logsigmoid(pos_score - neg_score)
        cf_loss = torch.mean(cf_loss)

        # L2 Loss
        l2_loss = _L2_loss_mean(user_embed) + _L2_loss_mean(item_pos_embed) + _L2_loss_mean(item_neg_embed)
        
        loss = cf_loss + self.l2loss_lambda * l2_loss
        return loss


    def forward(self, *input, is_train):
        if is_train:
            return self.calc_loss(*input)
        else:
            return self.calc_score(*input)


