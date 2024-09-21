import pandas as pd
import torch
import torch.nn as nn
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from torch.utils.data import DataLoader, TensorDataset
from DeepFM import DeepFM
from sklearn.metrics import ndcg_score
import warnings

warnings.filterwarnings('ignore')

full_info = pd.read_csv('../Dataset/movie_final_info.csv')

sparse_feature = ["Movie", "User", "Time"]
dense_feature = ["favor", "watched"]
# 填充缺失值
full_info[sparse_feature] = full_info[sparse_feature].fillna('-1')
# full_info["Tag"] = full_info["Tag"].fillna('-1')
full_info[dense_feature] = full_info[dense_feature].fillna(0)

# 离散特征
for feature in sparse_feature:
    label = LabelEncoder()
    full_info[feature] = label.fit_transform(full_info[feature])

# 数值特征归一化
mms = MinMaxScaler()
full_info[dense_feature] = mms.fit_transform(full_info[dense_feature])

# 分割数据集
# 先不管Tag
x_train, x_test, y_train, y_test = train_test_split(full_info[sparse_feature + dense_feature].values.astype(np.float32),
                                                    full_info["Rate"].values.astype(np.float32),
                                                    test_size=0.2,
                                                    random_state=2023)
# 用于生成文件/检验数据
# train = pd.concat([x_train, y_train], axis=1)
# train.to_csv("train.csv", index=False)
# test = pd.concat([x_test, y_test], axis=1)
# test.to_csv("test.csv", index=False)
# print(x_train)
# print("=========================================")
# print(x_test)
# print("=========================================")
# print(y_train)
# print("=========================================")
# print(y_test)

# 构建数据管道
train_dataset = TensorDataset(torch.tensor(x_train).float(), torch.tensor(y_train).float())
test_dataset = TensorDataset(torch.tensor(x_test).float(), torch.tensor(y_test).float())
train_loader = DataLoader(train_dataset, batch_size=4096, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=4096, shuffle=True)

# 训练
hidden = [128, 64, 32]
dropout = 0
feature_col = [[{"feature": feature_} for feature_ in dense_feature]] + [
    [{"feature": feature_, "feature_num": full_info[feature_].nunique(), "embedding_dim": 3} for feature_ in
     sparse_feature]]
model = DeepFM(hidden, feature_col, dropout)
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
num_epochs = 10

for epoch in range(num_epochs):
    # 训练
    model.train()
    loss_sum_train, loss_sum_test = 0.0, 0.0
    for i, (x, y) in enumerate(train_loader):
        optimizer.zero_grad()
        y_prediction = model(x)
        loss = criterion(y_prediction, y)
        loss.backward()
        optimizer.step()
        loss_sum_train += loss.item()
        output_loss_train = loss_sum_train / (i + 1)

    model.eval()
    y_list, y_prediction_list = [], []
    y_array, y_prediction_array = np.array([]), np.array([])
    with torch.no_grad():
        for index, (x_, y_) in enumerate(test_loader):
            y_prediction_ = model(x_)
            loss = criterion(y_prediction_, y_)
            y_list = torch.tensor(y_).numpy()
            # for array in y_list:
            #     y_array = np.append(y_array, array)
            y_array = np.append(y_array, y_list)
            # print(y_array.shape)
            y_prediction_list = torch.tensor(y_prediction_).numpy()
            # for array in y_prediction_list:
            #     y_prediction_array = np.append(y_prediction_array, array)
            y_prediction_array = np.append(y_prediction_array, y_prediction_)
            # print(y_prediction_array.shape)
            loss_sum_test += loss.item()
            output_loss_test = loss_sum_test / (i + 1)

    y_array = y_array.tolist()
    y_prediction_array = y_prediction_array.tolist()
    # print(y_array, type(y_array))
    # print(y_array.shape, y_prediction_array.shape)
    ndcgscore = ndcg_score([y_array], [y_prediction_array])
    print("epoch: {}, train_loss: {}, test_loss: {}, ndcg_score: {}".format(epoch + 1, output_loss_train,
                                                                            output_loss_test, ndcgscore))
