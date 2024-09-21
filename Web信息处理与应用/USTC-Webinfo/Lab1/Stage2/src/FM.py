import torch
import torch.nn as nn


class FM(nn.Module):
    # latent_dim是离散特征隐向量的维度, feature_num是特征的数量
    def __init__(self, feature_num, latent_dim):
        super(FM, self).__init__()
        self.latent_dim = latent_dim
        # 下面定义了三个矩阵
        self.w0 = nn.Parameter(torch.zeros([1, ]))
        self.w1 = nn.Parameter(torch.rand([feature_num, 1]))
        self.w2 = nn.Parameter(torch.rand([feature_num, latent_dim]))

    def forward(self, Input):
        # 一阶交叉
        order_1st = self.w0 + torch.mm(Input, self.w1)
        # 二阶交叉
        order_2nd = 1 / 2 * torch.sum(
            torch.pow(torch.mm(Input, self.w2), 2) - torch.mm(torch.pow(Input, 2), torch.pow(self.w2, 2)), dim=1,
            keepdim=True)
        return order_1st + order_2nd

