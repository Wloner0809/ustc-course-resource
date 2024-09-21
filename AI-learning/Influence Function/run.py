import pytorch_influence_functions as ptif
from dataset import get_mnist_loaders
from model_LR import LogisticRegression
import torch
import torch.optim as optim
from trainer import Trainer
import json


train_loader, valid_loader, test_loader, hessian_loader = get_mnist_loaders(1, 1)
"initialize model, criterion, optimizer and trainer here"
model = LogisticRegression(28 * 28, 10)
criterion = torch.nn.CrossEntropyLoss()
# optimizer = optim.LBFGS(model.parameters(), lr=0.001)
# # optimizer = optim.AdamW(model.parameters(), lr=0.001, weight_decay=0.01)
optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9, weight_decay=0.01)
# device = "cuda" if torch.cuda.is_available() else "cpu"
device = "cpu"
trainer = Trainer(model, optimizer, criterion, device)
trainer.train(train_loader, valid_loader, 10)
test_loss = trainer.test(test_loader)
trainer.save_model("model_sgd_retrain.pth")


"use stochastic hessian estimation version"
train_loader, valid_loader, test_loader, hessian_loader = get_mnist_loaders(1, 1)
model = LogisticRegression(28 * 28, 10)
trainer = Trainer(model, optimizer, criterion, "cuda")
trainer.load_model("model_sgd_retrain.pth")
ptif.init_logging()
config = ptif.get_default_config()
influences, test_id_num = ptif.calc_img_wise(
    config, trainer.model, hessian_loader, train_loader, test_loader
)


"leave one out retraining version"
loss_total = []
actual_diff = []
records = {}
for train_id in influences[str(test_id_num)]["max_abs_influence_id"]:
    train_loader, valid_loader, test_loader, hessian_loader = get_mnist_loaders(
        1, 1, True, train_id
    )
    model = LogisticRegression(28 * 28, 10)
    criterion = torch.nn.CrossEntropyLoss()
    # optimizer = optim.AdamW(model.parameters(), lr=0.001, weight_decay=0.01)
    optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9, weight_decay=0.01)
    # optimizer = optim.LBFGS(model.parameters(), lr=0.001)
    device = "cpu"
    trainer = Trainer(model, optimizer, criterion, device)
    trainer.load_model("model_sgd_retrain.pth")
    print(f"remove train sample {train_id}")
    trainer.train(train_loader, valid_loader, 1)
    "test the model here"
    inputs, targets = test_loader.dataset[test_id_num]
    inputs = test_loader.collate_fn([inputs])
    targets = test_loader.collate_fn([targets])
    inputs = inputs.view(-1, 28 * 28)
    # NOTE: normalize the inputs
    # inputs = inputs / 255.0
    inputs, targets = inputs.to(device), targets.to(device)
    model = trainer.model.to(device)
    outputs = model(inputs)
    loss = criterion(outputs, targets)
    loss_total.append(loss.item())
    actual_diff.append(loss.item() - test_loss[test_id_num])
    "store the results here"
    records[train_id] = {}
    records[train_id]["loss"] = loss.item()
    records[train_id]["actual_diff"] = loss.item() - test_loss[test_id_num]
    records[train_id]["influence"] = influences[str(test_id_num)]["influence"][train_id]
    print(
        f"actual_diff: {loss.item() - test_loss[test_id_num]}, predicted_diff: {influences[str(test_id_num)]['influence'][train_id]}"
    )

with open("./results/compare_sgd_retrain.json", "w") as f:
    json.dump(records, f, indent=2)


# from sklearn import linear_model
# from dataset import get_mnist_data
# import numpy as np


# class LogisticRegression(torch.nn.Module):
#     def __init__(self):
#         super(LogisticRegression, self).__init__()
#         self.w = torch.nn.Parameter(torch.zeros([10, 784], requires_grad=True))

#     def forward(self, x):
#         logits = torch.matmul(x, self.w.T)
#         return logits

#     def loss(self, logits, y, train=True):
#         criterion = torch.nn.CrossEntropyLoss()
#         # set dtype to float
#         y = y.type(torch.FloatTensor)
#         loss = criterion(logits, y.long())
#         return loss


# (x_train, y_train), (x_test, y_test) = get_mnist_data()
# sklearn_model = linear_model.LinearRegression(
#     C=1.0 / (len(x_train) * 0.01),
#     fit_intercept=False,
#     solver="lbfgs",
#     tol=1e-8,
#     multi_class="multinomial",
#     warm_start=True,
# )
# sklearn_model.fit(x_train, y_train.ravel())
# w_opt = torch.tensor(sklearn_model.coef_, requires_grad=True, dtype=torch.float32)
# torch_model = LogisticRegression()
# with torch.no_grad():
#     torch_model.w = torch.nn.Parameter(w_opt)

# x_test_input = torch.FloatTensor(x_test[test_id_num: test_id_num + 1])
# y_test_input = torch.LongTensor(y_test[test_id_num: test_id_num + 1])
# test_loss = torch_model.loss(torch_model(x_test_input), y_test_input, train=False).cpu().detach().numpy()
# for train_id in influences[str(test_id_num)]["max_abs_influence_id"]:
#     x_train_remove = np.delete(x_train, train_id, axis=0)
#     y_train_remove = np.delete(y_train, train_id, axis=0)
#     sklearn_model = linear_model.LinearRegression(
#         C=1.0 / (len(x_train_remove) * 0.01),
#         fit_intercept=False,
#         solver="lbfgs",
#         tol=1e-8,
#         multi_class="multinomial",
#         warm_start=True,
#     )
#     sklearn_model.fit(x_train_remove, y_train_remove.ravel())
#     w_opt = torch.tensor(sklearn_model.coef_, requires_grad=True, dtype=torch.float32)
#     with torch.no_grad():
#         torch_model.w = torch.nn.Parameter(w_opt)
#     test_loss_remove = torch_model.loss(torch_model(x_test_input), y_test_input, train=False).cpu().detach().numpy()
#     print(f"actual_diff: {test_loss_remove - test_loss}, predicted_diff: {influences[str(test_id_num)]['influence'][train_id]}")
