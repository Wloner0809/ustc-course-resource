from torchvision.datasets import MNIST
from torchvision import transforms
from torch.utils.data import DataLoader, RandomSampler
from torch.utils.data import random_split, Subset


def remove_one_sample(train_data, train_id):
    indices = list(range(len(train_data)))
    indices.remove(train_id)
    train_data = Subset(train_data, indices)
    return train_data


def get_mnist_loaders(
    train_batch_size,
    test_batch_size,
    leave_one_out=False,
    train_id=0,
    recursion_depth=5000,
):
    mnist_train = MNIST(
        "./data/train", train=True, download=True, transform=transforms.ToTensor()
    )
    mnist_test = MNIST(
        "./data/test", train=False, download=True, transform=transforms.ToTensor()
    )
    train_data, valid_data = random_split(mnist_train, [55000, 5000])
    if leave_one_out:
        train_data = remove_one_sample(train_data, train_id)
    train_loader = DataLoader(train_data, batch_size=train_batch_size, shuffle=True)
    valid_loader = DataLoader(valid_data, batch_size=train_batch_size, shuffle=False)
    "add hessian loader here used in stochastic estimation of hvp"
    # TODO: call get_mnist_loaders() once so we get same hessian_loader
    hessian_loader = DataLoader(
        mnist_train,
        sampler=RandomSampler(
            mnist_train, replacement=True, num_samples=recursion_depth
        ),
    )
    test_loader = DataLoader(mnist_test, batch_size=test_batch_size, shuffle=False)
    return train_loader, valid_loader, test_loader, hessian_loader


def get_mnist_data():
    mnist_train = MNIST(
        "./data/train", train=True, download=True, transform=transforms.ToTensor()
    )
    mnist_test = MNIST(
        "./data/test", train=False, download=True, transform=transforms.ToTensor()
    )
    x_train = mnist_train.data[:-5000]
    y_train = mnist_train.targets
    x_train = x_train.view(-1, 28 * 28)
    x_test = mnist_test.data[:-5000]
    y_test = mnist_test.targets
    x_test = x_test.view(-1, 28 * 28)
    return (x_train, y_train), (x_test, y_test)
