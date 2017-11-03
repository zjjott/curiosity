# coding=utf-8
from __future__ import unicode_literals, absolute_import
from keras.layers import Conv2D, BatchNormalization
from torch import nn
from keras.models import Sequential


class DQN2(nn.Module):

    def __init__(self):
        super(DQN, self).__init__()
        self.conv1 = nn.Conv2d(3, 16, kernel_size=5, stride=2)
        self.bn1 = nn.BatchNorm2d(16)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=5, stride=2)
        self.bn2 = nn.BatchNorm2d(32)
        self.conv3 = nn.Conv2d(32, 32, kernel_size=5, stride=2)
        self.bn3 = nn.BatchNorm2d(32)
        self.head = nn.Linear(448, 2)

    def forward(self, x):
        x = F.relu(self.bn1(self.conv1(x)))
        x = F.relu(self.bn2(self.conv2(x)))
        x = F.relu(self.bn3(self.conv3(x)))
        return self.head(x.view(x.size(0), -1))


class DQN(object):
    def __init__(self, width, heigh):
        model = Sequential()
        model.add(Conv2D((2, 2),
                         kernel_size=5,
                         stride=2), input_shape=(3, width, heigh))
        model.add(BatchNormalization())
        model.add(Conv2D((3, 3),
                         kernel_size=5,
                         stride=2), input_shape=(3, width, heigh))
