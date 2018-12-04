
# --------------------------------------------------------------------------------------------
import torch
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
import numpy as np
import torch.nn as nn
from torch.autograd import Variable
import torch.optim as optim


num_classes = 100
num_epochs = 40
batch_size = 100
learning_rate = 0.001

momentum = 0.9
# --------------------------------------------------------------------------------------------
transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
# --------------------------------------------------------------------------------------------

train_set = torchvision.datasets.CIFAR100(root='./data_cifar', train=True, download=True, transform=transform)

train_loader = torch.utils.data.DataLoader(train_set, batch_size=batch_size, shuffle=True)

testset = torchvision.datasets.CIFAR100(root='./data_cifar', train=False, download=True, transform=transform)

test_loader = torch.utils.data.DataLoader(testset, batch_size=batch_size, shuffle=False)

classes = ['beaver', 'dolphin', 'otter', 'seal', 'whale',
    'aquarium fish', 'flatfish', 'ray', 'shark', 'trout',
    'orchids', 'poppies', 'roses', 'sunflowers', 'tulips',
    'bottles', 'bowls', 'cans', 'cups', 'plates',
    'apples', 'mushrooms', 'oranges', 'pears', 'sweet peppers',
    'clock', 'computer keyboard', 'lamp', 'telephone', 'television',
    'bed', 'chair', 'couch', 'table', 'wardrobe',
    'bee', 'beetle', 'butterfly', 'caterpillar', 'cockroach',
    'bear', 'leopard', 'lion', 'tiger', 'wolf',
    'bridge', 'castle', 'house', 'road', 'skyscraper',
    'cloud', 'forest', 'mountain', 'plain','sea',
    'camel', 'cattle', 'chimpanzee', 'elephant', 'kangaroo',
    'fox', 'porcupine', 'possum', 'raccoon', 'skunk',
    'crab', 'lobster', 'snail', 'spider', 'worm',
    'baby', 'boy', 'girl', 'man', 'woman',
    'crocodile', 'dinosaur', 'lizard', 'snake', 'turtle',
    'hamster', 'mouse', 'rabbit', 'shrew', 'squirrel',
    'maple', 'oak', 'palm', 'pine', 'willow',
    'bicycle', 'bus', 'motorcycle', 'pickup truck', 'train',
    'lawn-mower', 'rocket', 'streetcar', 'tank', 'tractor']


# --------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------

class SimpleNet(nn.Module):

    def __init__(self, num_classes=100):
        super(SimpleNet, self).__init__()
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=30, kernel_size=5)
        self.relu = nn.ReLU()
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)

        self.conv2 = nn.Conv2d(in_channels=30, out_channels=80, kernel_size=5)
        self.fc1 = nn.Linear(80* 10* 10, 120)# flatern
        self.fc2 = nn.Linear(120,110)
        self.fc3 = nn.Linear(110, num_classes)

    def forward(self, x):
        out = self.pool(self.relu(self.conv1(x)))
        out = self.relu(self.conv2(out))

        out=out.view(-1,80*10*10)

        out = self.relu(self.fc1(out))
        out = self.relu(self.fc2(out))
        out = self.fc3(out)
        return out
# --------------------------------------------------------------------------------------------


# Choose the right argument for x                                           # error5: choose x
cnn = SimpleNet(num_classes)
cnn.cuda()
# --------------------------------------------------------------------------------------------
# Choose the right argument for x
criterion = nn.CrossEntropyLoss()                                                  # (use different) Loss function
optimizer = optim.SGD(cnn.parameters(), lr=learning_rate, momentum=momentum)    # (use different) Optimizer
# --------------------------------------------------------------------------------------------
# There is bug here find it and fix it
loss_1=[]
import time
start = time.clock()

for epoch in range(num_epochs):
    for i, data in enumerate(train_loader):

        images, labels = data
        #images = images.view(-1, 3 * 32 * 32)                    # error6: the dimension of input should be 3*32*32
        images, labels = Variable(images.cuda()), Variable(labels.cuda())

        optimizer.zero_grad()
        outputs = cnn(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        loss_1.append(loss.item())

        if (i + 1) % 100 == 0:
            print('Epoch [%d/%d], Step [%d/%d], Loss: %.4f'
                  % (epoch + 1, num_epochs, i + 1, len(train_set) // batch_size, loss.item()))


end = time.clock()
print("time used", end-start)
# --------------------------------------------------------------------------------------------

# Test the Model

cnn.eval()
correct = 0
total = 0
for images, labels in test_loader:
    images = Variable(images.cuda())
    labels = Variable(labels.cuda())                        # error8: the dimension of input
    outputs = cnn(images)
    _, predicted = torch.max(outputs.data, 1)
    total += labels.size(0)
    correct += torch.sum((predicted == labels)).cpu().numpy()

print('Accuracy of the network on the 10000 test images: %d %%' % (100 * correct / total))
# --------------------------------------------------------------------------------------------
##plot training loss

plt.figure("loss function")
plt.plot(loss_1)
plt.show()

## test for getting CONV picture

print("test start")


torch.save(cnn.state_dict(), 'model.pkl')