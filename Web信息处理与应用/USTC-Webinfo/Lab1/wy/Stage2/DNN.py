import torch.nn.functional as F
import torch.nn as nn


class DNN(nn.Module):
    def __init__(self, hidden, dropout=0):
        super(DNN, self).__init__()
        # 相邻的hidden层, Linear用于设置全连接层
        # ModuleList可以将nn.Module的子类加入到List中
        self.dnn = nn.ModuleList([nn.Linear(layer[0], layer[1]) for layer in list(zip(hidden[:-1], hidden[1:]))])
        # dropout用于训练, 代表前向传播中有多少概率神经元不被激活
        # 为了减少过拟合
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        for linear in self.dnn:
            x = linear(x)
            # relu激活函数
            x = F.relu(x)
        x = self.dropout(x)
        return x
