import sys
import copy
import random
import numpy as np
import torch
from collections import defaultdict
from multiprocessing import Process, Queue


# sampler for batch generation
def random_neq(l, r, s):  # noqa: E741
    t = np.random.randint(l, r)
    while t in s:
        t = np.random.randint(l, r)
    return t


def sample_function(
    user_train, usernum, itemnum, batch_size, maxlen, result_queue, SEED
):
    def sample():
        user = np.random.randint(1, usernum + 1)
        while len(user_train[user]) <= 1:
            user = np.random.randint(1, usernum + 1)

        seq = np.zeros([maxlen], dtype=np.int32)
        pos = np.zeros([maxlen], dtype=np.int32)
        neg = np.zeros([maxlen], dtype=np.int32)
        nxt = user_train[user][-1]
        idx = maxlen - 1

        ts = set(user_train[user])
        for i in reversed(user_train[user][:-1]):
            seq[idx] = i
            pos[idx] = nxt
            if nxt != 0:
                neg[idx] = random_neq(1, itemnum + 1, ts)
            nxt = i
            idx -= 1
            if idx == -1:
                break

        return (user, seq, pos, neg)

    np.random.seed(SEED)
    while True:
        one_batch = []
        for i in range(batch_size):
            one_batch.append(sample())

        result_queue.put(zip(*one_batch))


class WarpSampler(object):
    def __init__(self, User, usernum, itemnum, batch_size=64, maxlen=10, n_workers=1):
        self.result_queue = Queue(maxsize=n_workers * 10)
        self.processors = []
        for i in range(n_workers):
            self.processors.append(
                Process(
                    target=sample_function,
                    args=(
                        User,
                        usernum,
                        itemnum,
                        batch_size,
                        maxlen,
                        self.result_queue,
                        np.random.randint(2e9),
                    ),
                )
            )
            self.processors[-1].daemon = True
            self.processors[-1].start()

    def next_batch(self):
        return self.result_queue.get()

    def close(self):
        for p in self.processors:
            p.terminate()
            p.join()


# 用于分割数据集
def data_partition(fname):
    usernum = 0
    itemnum = 0
    User = defaultdict(list)
    user_train = {}
    user_valid = {}
    user_test = {}
    # assume user/item index starting from 1
    f = open("data/%s.txt" % fname, "r")
    for line in f:
        u, i = line.rstrip().split(" ")
        u = int(u)
        i = int(i)
        usernum = max(u, usernum)
        itemnum = max(i, itemnum)
        User[u].append(i)

    for user in User:
        nfeedback = len(User[user])
        if nfeedback < 3:
            user_train[user] = User[user]
            user_valid[user] = []
            user_test[user] = []
        else:
            user_train[user] = User[user][:-2]
            user_valid[user] = []
            user_valid[user].append(User[user][-2])
            user_test[user] = []
            user_test[user].append(User[user][-1])
    return [user_train, user_valid, user_test, usernum, itemnum]


# evaluate on test set
def evaluate(model, dataset, args):
    [train, valid, test, usernum, itemnum] = copy.deepcopy(dataset)
    topk = [1, 3, 5, 10, 20]
    if usernum > 5100:
        random.seed(0)
        users = random.sample(range(1, usernum + 1), 5100)
    else:
        users = range(1, usernum + 1)
    test_user = 0.0
    ndcg_list = [0.0, 0.0, 0.0, 0.0, 0.0]
    hr_list = [0.0, 0.0, 0.0, 0.0, 0.0]
    predict_test = torch.tensor([]).cuda()
    for u in users:
        if len(train[u]) < 1 or len(test[u]) < 1:
            continue

        seq = np.zeros([args.maxlen], dtype=np.int32)
        idx = args.maxlen - 1
        seq[idx] = valid[u][0]
        idx -= 1
        for i in reversed(train[u]):
            seq[idx] = i
            idx -= 1
            if idx == -1:
                break
        rated = set(train[u])
        rated.add(0)
        item_idx = [test[u][0]]
        for _ in range(14238):
            t = np.random.randint(1, itemnum + 1)
            while t in rated:
                t = np.random.randint(1, itemnum + 1)
            item_idx.append(t)

        predictions = -model.predict(*[np.array(l) for l in [[u], [seq], item_idx]])  # noqa: E741
        predictions = predictions[0]  # - for 1st argsort DESC
        predict_test = torch.cat((predict_test, predictions.unsqueeze(0)), dim=0)

        rank = predictions.argsort().argsort()[0].item()

        test_user += 1
        for i, k in enumerate(topk):
            if rank < k:
                ndcg_list[i] += 1 / np.log2(rank + 2)
                hr_list[i] += 1
        if test_user % 500 == 0:
            print(".", end="")
            sys.stdout.flush()
        if test_user == 5000:
            break
    torch.save(predict_test, "test.pt")
    del predict_test
    torch.cuda.empty_cache()
    ndcg_list = [ndcg / test_user for ndcg in ndcg_list]
    hr_list = [hr / test_user for hr in hr_list]

    return ndcg_list, hr_list


# evaluate on val set
def evaluate_valid(model, dataset, args):
    [train, valid, test, usernum, itemnum] = copy.deepcopy(dataset)
    topk = [1, 3, 5, 10, 20]
    if usernum > 5100:
        random.seed(0)
        users = random.sample(range(1, usernum + 1), 5100)
    else:
        users = range(1, usernum + 1)
    ndcg_list = [0.0, 0.0, 0.0, 0.0, 0.0]
    hr_list = [0.0, 0.0, 0.0, 0.0, 0.0]
    predict_val = torch.tensor([]).cuda()
    valid_user = 0.0
    for u in users:
        if len(train[u]) < 1 or len(valid[u]) < 1:
            continue

        seq = np.zeros([args.maxlen], dtype=np.int32)
        idx = args.maxlen - 1
        for i in reversed(train[u]):
            seq[idx] = i
            idx -= 1
            if idx == -1:
                break

        rated = set(train[u])
        rated.add(0)
        item_idx = [valid[u][0]]
        for _ in range(14238):
            t = np.random.randint(1, itemnum + 1)
            while t in rated:
                t = np.random.randint(1, itemnum + 1)
            item_idx.append(t)

        predictions = -model.predict(*[np.array(l) for l in [[u], [seq], item_idx]])  # noqa: E741
        predictions = predictions[0]
        predict_val = torch.cat((predict_val, predictions.unsqueeze(0)), dim=0)

        rank = predictions.argsort().argsort()[0].item()

        valid_user += 1

        for i, k in enumerate(topk):
            if rank < k:
                ndcg_list[i] += 1 / np.log2(rank + 2)
                hr_list[i] += 1
        if valid_user % 500 == 0:
            print(".", end="")
            sys.stdout.flush()
        if valid_user == 5000:
            break
    torch.save(predict_val, "val.pt")
    del predict_val
    torch.cuda.empty_cache()
    ndcg_list = [ndcg / valid_user for ndcg in ndcg_list]
    hr_list = [hr / valid_user for hr in hr_list]

    return ndcg_list, hr_list
