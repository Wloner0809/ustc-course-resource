import numpy as np
from sklearn.metrics import log_loss
from sklearn.metrics import accuracy_score
from tqdm import trange


class LinearActive:
    def __init__(self, cryptosystem, messenger, *, epochs=100, batch_size=100, learning_rate=0.1):
        self.cryptosystem = cryptosystem
        self.messenger = messenger
        self.epochs = epochs
        self.batch_size = batch_size
        self.learning_rate = learning_rate
        self.reg_lambda = 0.01

        self.RESIDUE_PRECISION = 3
        self.activation = lambda x: 1.0 / (1.0 + np.exp(-x))

    def _sync_pubkey(self):
        signal = self.messenger.recv()
        if signal == "START_SIGNAL":
            print("Training protocol started.")
            print("[ACTIVE] Sending public key to passive party...")
            self.messenger.send(self.cryptosystem.pub_key)
        else:
            raise ValueError("Invalid signal, exit.")
        print("[ACTIVE] Sending public key done!")

    def _gradient(self, residue, batch_idxes):
        data_grad = self._data_grad_naive(residue, batch_idxes)
        reg_grad = self._reg_grad()
        return data_grad + reg_grad

    def _data_grad_naive(self, residue, batch_idxes):
        data_grad = -1 * (residue[:, np.newaxis] * self.x_train[batch_idxes]).mean(axis=0)
        return data_grad

    def train(self, trainset):
        self.x_train = trainset.features
        self.y_train = trainset.labels
        self.y_val = trainset.labels

        # initialize model parameters
        self._init_weights(trainset.n_features)

        # transmit public key to passive party
        self._sync_pubkey()

        bs = self.batch_size if self.batch_size != -1 else trainset.n_samples
        n_samples = trainset.n_samples
        if n_samples % bs == 0:
            n_batches = n_samples // bs
        else:
            n_batches = n_samples // bs + 1

        # Main Training Loop Here
        tbar = trange(self.epochs)
        loss_record = [[]]
        acc_record = [[]]
        for epoch in tbar:
            # 等价代码
            # -----------------------------------------------------------------
            # random_state = np.random.RandomState(epoch)
            # all_idxes = np.arange(n_samples)
            # random_state.shuffle(all_idxes)
            # -----------------------------------------------------------------
            
            # 原始代码
            all_idxes = np.arange(n_samples)
            np.random.seed(epoch)
            np.random.shuffle(all_idxes)
            
            # 记录loss和acc
            loss_epoch = []
            acc_epoch = []

            for batch in range(n_batches):
                # Choose batch indexes
                start = batch * bs
                end = len(all_idxes) if batch == n_batches - 1 else (batch + 1) * bs
                batch_idxes = all_idxes[start:end]

                # Q1. Active party calculates y_hat
                # -----------------------------------------------------------------
                # TODO
                active_wx = np.dot(self.x_train[batch_idxes], self.params)  
                passive_wx = self.messenger.recv()
                # TODO
                full_wx = active_wx + passive_wx  
                y_hat = self.activation(full_wx)
                # -----------------------------------------------------------------

                loss = self._loss(self.y_train[batch_idxes], y_hat)
                acc = self._acc(self.y_train[batch_idxes], y_hat)
                tbar.set_description(f"[loss={loss:.4f}, acc={acc:.4f}]")
                
                # 记录loss和acc
                loss_epoch.append(loss)
                acc_epoch.append(acc)
                
                residue = self.y_train[batch_idxes] - y_hat
                residue = np.array([round(res, self.RESIDUE_PRECISION) for res in residue])

                # Q2. Active party helps passive party to calculate gradient
                # -----------------------------------------------------------------
                # TODO
                enc_residue = self.cryptosystem.encrypt_vector(residue)
                enc_residue = np.array(enc_residue)
                self.messenger.send(enc_residue)
                enc_passive_grad = self.messenger.recv()
                # TODO
                passive_grad = np.array(self.cryptosystem.decrypt_vector(enc_passive_grad))
                self.messenger.send(passive_grad)
                # -----------------------------------------------------------------

                # Active party calculates its own gradient and update model
                active_grad = self._gradient(residue, batch_idxes)
                self._gradient_descent(self.params, active_grad)
            
            # 记录loss和acc
            loss_record.append(loss_epoch)
            acc_record.append(acc_epoch)

        print("Finish model training.")
        print(loss_record)
        print(acc_record)

    def _init_weights(self, size):
        np.random.seed(0)
        self.params = np.random.normal(0, 1.0, size)

    def _reg_grad(self):
        params = self.params
        reg_grad = self.reg_lambda * params
        return reg_grad

    def _gradient_descent(self, params, grad):
        params -= self.learning_rate * grad

    def _loss(self, y_true, y_hat):
        # Logistic regression uses log-loss as loss function
        data_loss = self._logloss(y_true, y_hat)
        reg_loss = self._reg_loss()
        total_loss = data_loss + reg_loss

        return total_loss

    def _acc(self, y_true, y_hat):
        # Q3. Compute accuracy
        # -----------------------------------------------------------------
        # TODO
        acc = accuracy_score(y_true=y_true, y_pred=y_hat.round()) # 调用sklearn的accuracy_score函数
        # -----------------------------------------------------------------
        return acc

    @staticmethod
    def _logloss(y_true, y_hat):
        origin_size = len(y_true)
        if len(np.unique(y_true)) == 1:
            if y_true[0] == 0:
                y_true = np.append(y_true, 1)
                y_hat = np.append(y_hat, 1.0)
            else:
                y_true = np.append(y_true, 0)
                y_hat = np.append(y_hat, 0.0)

        return log_loss(y_true=y_true, y_pred=y_hat, normalize=False) / origin_size

    def _reg_loss(self):
        params = self.params
        reg_loss = 1.0 / 2 * self.reg_lambda * (params**2).sum()
        return reg_loss
