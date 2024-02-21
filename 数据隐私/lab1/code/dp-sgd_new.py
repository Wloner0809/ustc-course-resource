import numpy as np
from sklearn.datasets import make_classification, load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import argparse
import math

RANDOM_STATE = 1

class LogisticRegressionCustom:
    def __init__(self, learning_rate=0.01, num_iterations=100):
        self.learning_rate = learning_rate
        self.num_iterations = num_iterations
        self.tau = 1e-6  # small value to prevent log(0)
        self.weights = None
        self.bias = None

    def sigmoid(self, z):
        # np.clip(z, -500, 500) limits the range of z to avoid extremely 
        # large or small values that could lead to overflow.
        return 1 / (1 + np.exp(-np.clip(z, -700, 700)))

    def fit(self, X, y):
        # Initialize weights and bias
        num_samples, num_features = X.shape
        self.weights = np.zeros(num_features)
        self.bias = 0.0

        # Gradient descent optimization
        for _ in range(self.num_iterations):
            # Compute predictions of the model
            linear_model = np.dot(X, self.weights) + self.bias
            predictions = self.sigmoid(linear_model)

            # Compute loss and gradients
            loss = -np.mean(
                y * np.log(predictions + self.tau)
                + (1 - y) * np.log(1 - predictions + self.tau)
            )
            dz = predictions - y
            dw = np.dot(X.T, dz) / num_samples
            db = np.sum(dz) / num_samples

            # Update weights and bias
            self.weights -= self.learning_rate * dw
            self.bias -= self.learning_rate * db

    def dp_fit(self, X, y, epsilon, delta, C=1):
        # Initialize weights and bias
        num_samples, num_features = X.shape  # X.shape = (455, 30)
        self.weights = np.zeros(num_features)
        self.bias = 0

        # Gradient descent optimization
        for _ in range(self.num_iterations):
            # Compute predictions of the model
            linear_model = np.dot(X, self.weights) + self.bias  # (455, )
            predictions = self.sigmoid(linear_model)

            # Compute loss and gradients
            loss = -np.mean(y * np.log(predictions + self.tau) + (1 - y) * np.log(1 - predictions + self.tau))
            dz = -(y / (predictions + self.tau) - (1 - y) / (1 - predictions + self.tau)) # Cross entropy loss
            dz = dz * (predictions * (1 - predictions)) # sigmoid derivative

            # TODO: Clip gradient here.
            clip_dz = clip_gradients(dz, C)
            # Add noise to gradients
            # TODO: Calculate epsilon_u, delta_u based epsilon, delta and epochs here.
            delta_u = delta / (self.num_iterations + 1)
            epsilon_u = epsilon / (2 * math.sqrt(2 * self.num_iterations * math.log(1 / delta_u)))
            # epsilon_u, delta_u = epsilon / self.num_iterations, delta / self.num_iterations
            noisy_dz = add_gaussian_noise_to_gradients(clip_dz, epsilon_u, delta_u, C)

            dw = np.dot(X.T, noisy_dz) / num_samples  # (30, )
            db = np.sum(noisy_dz) / num_samples  # 直接计算平均bias

            # Update weights and bias
            self.weights -= self.learning_rate * dw
            self.bias -= self.learning_rate * db

    def predict_probability(self, X):
        linear_model = np.dot(X, self.weights) + self.bias
        probabilities = self.sigmoid(linear_model)
        return probabilities

    def predict(self, X):
        probabilities = self.predict_probability(X)
        # Convert probabilities to classes
        return np.round(probabilities)


def get_train_data(dataset_name=None):
    if dataset_name is None:
        # Generate simulated data
        np.random.seed(RANDOM_STATE)
        X, y = make_classification(
            n_samples=1000, n_features=20, n_classes=2, random_state=RANDOM_STATE
        )
    elif dataset_name == "cancer":
        # Load the breast cancer dataset
        data = load_breast_cancer()
        X, y = data.data, data.target
    else:
        raise ValueError("Not supported dataset_name.")
    
    # normalize the data
    X = (X - np.mean(X, axis=0)) / X.std(axis=0)

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE
    )
    return X_train, X_test, y_train, y_test


def clip_gradients(dz, C):
    # TODO: Clip gradients.
    dz_norm = np.linalg.norm(dz)
    dz_max = max(1, dz_norm / C)
    clip_dz = dz / dz_max
    return clip_dz


def add_gaussian_noise_to_gradients(clip_dz, epsilon, delta, C):
    # TODO: add gaussian noise to gradients.
    sigma = np.sqrt(2 * np.log(1.25 / delta)) * C / epsilon  # sigma是最终的标准差
    noise = np.random.normal(0, sigma, clip_dz.shape)
    noisy_dz = clip_dz + noise
    return noisy_dz


if __name__ == "__main__":
    # Prepare datasets.
    dataset_name = "cancer"
    X_train, X_test, y_train, y_test = get_train_data(dataset_name)
    
    # 命令行传参
    parser = argparse.ArgumentParser()
    parser.add_argument('--epsilon', type=float, default=1)
    parser.add_argument('--delta', type=float, default=0.001)
    parser.add_argument('--iter', type=int, default=5000)
    args = parser.parse_args()
    epsilon = args.epsilon
    delta = args.delta
    iteration = args.iter

    # Training the normal model
    normal_model = LogisticRegressionCustom(learning_rate=0.01, num_iterations=iteration)
    normal_model.fit(X_train, y_train)
    y_pred = normal_model.predict(X_test)
    accuracy_normal = accuracy_score(y_test, y_pred)
    print(accuracy_normal)

    # Training the differentially private model
    dp_model = LogisticRegressionCustom(learning_rate=0.01, num_iterations=iteration)
    dp_model.dp_fit(X_train, y_train, epsilon=epsilon, delta=delta, C=1)
    y_pred = dp_model.predict(X_test)
    accuracy_dp = accuracy_score(y_test, y_pred)
    print(accuracy_dp)
