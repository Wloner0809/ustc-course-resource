import torch
from tqdm import tqdm


class Trainer:
    def __init__(self, model, optimizer, criterion, device):
        self.model = model.to(device)
        self.optimizer = optimizer
        self.criterion = criterion
        self.device = device

    def train(self, train_loader, valid_loader, epoch):
        train_loss = 0
        valid_loss = 0
        for epoch in tqdm(range(epoch)):
            self.model.train()
            train_loss = 0
            valid_loss = 0
            for inputs, targets in tqdm(train_loader):
                inputs = inputs.view(-1, 28 * 28)
                # inputs = inputs / 255.0
                inputs, targets = inputs.to(self.device), targets.to(self.device)
                def closure():
                    self.optimizer.zero_grad()
                    outputs = self.model(inputs)
                    loss = self.criterion(outputs, targets)
                    loss.backward()
                    return loss
                self.optimizer.step(closure)
            #     self.optimizer.zero_grad()
            #     outputs = self.model(inputs)
            #     loss = self.criterion(outputs, targets)
            #     loss.backward()
            #     self.optimizer.step()
            #     train_loss += loss.item()
            # print(
            #     "\nTrain Epoch: {} | Loss: {:.3f}".format(
            #         epoch, train_loss / len(train_loader)
            #     )
            # )

            self.model.eval()
            with torch.no_grad():
                for inputs, targets in tqdm(valid_loader):
                    inputs = inputs.view(-1, 28 * 28)
                    # inputs = inputs / 255.0
                    inputs, targets = inputs.to(self.device), targets.to(self.device)
                    outputs = self.model(inputs)
                    loss = self.criterion(outputs, targets)
                    valid_loss += loss.item()
                print(
                    "Valid Epoch: {} | Loss: {:.3f}".format(
                        epoch, valid_loss / len(valid_loader)
                    )
                )

    def test(self, test_loader) -> list:
        self.model.eval()
        test_loss = []
        correct = 0
        total = 0
        with torch.no_grad():
            for inputs, targets in tqdm(test_loader):
                inputs = inputs.view(-1, 28 * 28)
                # inputs = inputs / 255.0
                inputs, targets = inputs.to(self.device), targets.to(self.device)
                outputs = self.model(inputs)
                loss = self.criterion(outputs, targets)
                test_loss.append(loss.item())
                "calculate accuracy here"
                _, predicted = torch.max(outputs.data, 1)
                total += targets.size(0)
                correct += predicted.eq(targets).sum().item()

            print(
                "Test loss: {:.3f} | Acc: {:.3f}".format(
                    sum(test_loss) / len(test_loss), 100.0 * correct / total
                )
            )
        return test_loss

    def save_model(self, path):
        torch.save(self.model.state_dict(), path)
        print(f"Model saved to {path}")

    def load_model(self, path):
        self.model.load_state_dict(torch.load(path))
        print(f"Model loaded from {path}")
        self.model.to(self.device)
        return self.model
