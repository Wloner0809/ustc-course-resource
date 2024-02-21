import numpy as np
from tqdm import trange

from paillier import PartialPaillier, encode


class LinearPassive:
    def __init__(self, messenger, *, epochs=100, batch_size=100, learning_rate=0.1):
        self.messenger = messenger
        self.epochs = epochs
        self.batch_size = batch_size
        self.learning_rate = learning_rate

        self.reg_lambda = 0.01
        self.encode_precision = 0.001

    def _sync_pubkey(self):
        signal = "START_SIGNAL"
        self.messenger.send(signal)
        public_key = self.messenger.recv()
        return public_key

    def _gradient(self, enc_residue, batch_idxes):
        # compute data gradient
        enc_data_grad = self._data_grad_naive(enc_residue, batch_idxes)

        # computer regularization gradient
        reg_grad = self._reg_grad()

        enc_reg_grad = np.array(self.cryptosystem.encrypt_vector(reg_grad))

        return enc_data_grad + enc_reg_grad

    def _data_grad_naive(self, enc_residue, batch_idxes):
        data = self.x_encode
        enc_train_grad = -1 * (enc_residue[:, np.newaxis] * data[batch_idxes]).mean(axis=0)

        return enc_train_grad

    def _reg_grad(self):
        params = self.params
        reg_grad = self.reg_lambda * params
        return reg_grad

    def _mask_grad(self, enc_grad):
        # TODO
        mask = np.random.normal(0, 1.0, enc_grad.shape) # 正态分布随机数
        # TODO
        enc_mask_grad = enc_grad + np.array(self.cryptosystem.encrypt_vector(mask)) 
        return enc_mask_grad, mask

    def _unmask_grad(self, mask_grad, mask):
        # TODO
        true_grad = mask_grad - mask # 这里的mask没有加密
        return true_grad

    def train(self, trainset):
        self.x_train = trainset.features

        # init model parameters
        self._init_weights(trainset.n_features)

        # obtain public key from active party and init cryptosystem
        public_key = self._sync_pubkey()
        self.cryptosystem = PartialPaillier(public_key)

        # encode the training dataset
        x_encode, x_encode_mappings = encode(
            raw_data=getattr(self, "x_train"),
            raw_pub_key=public_key,
            precision=self.encode_precision,
        )
        self.x_encode = x_encode
        self.x_encode_mappings = np.array(x_encode_mappings)

        bs = self.batch_size if self.batch_size != -1 else trainset.n_samples
        n_samples = trainset.n_samples
        if n_samples % bs == 0:
            n_batches = n_samples // bs
        else:
            n_batches = n_samples // bs + 1

        # Main Training Loop Here
        for epoch in trange(self.epochs):
            all_idxes = np.arange(n_samples)
            np.random.seed(epoch)
            np.random.shuffle(all_idxes)

            for batch in range(n_batches):
                # Choose batch indexes
                start = batch * bs
                end = len(all_idxes) if batch == n_batches - 1 else (batch + 1) * bs
                batch_idxes = all_idxes[start:end]

                # Q1. Calculate wx and send it to active party
                # -----------------------------------------------------------------
                # TODO
                passive_wx = np.dot(self.x_train[batch_idxes], self.params)
                self.messenger.send(passive_wx)
                # -----------------------------------------------------------------

                # Q2. Receive encrypted residue and calculate masked encrypted gradients
                # -----------------------------------------------------------------
                enc_residue = self.messenger.recv()
                enc_grad = self._gradient(enc_residue, batch_idxes)
                enc_mask_grad, mask = self._mask_grad(enc_grad)
                self.messenger.send(enc_mask_grad)
                # Receive decrypted masked gradient and update model
                mask_grad = self.messenger.recv()
                true_grad = self._unmask_grad(mask_grad, mask)
                # -----------------------------------------------------------------

                self._gradient_descent(self.params, true_grad)

    def _init_weights(self, size):
        np.random.seed(0)
        self.params = np.random.normal(0, 1.0, size)

    def _gradient_descent(self, params, grad):
        params -= self.learning_rate * grad
