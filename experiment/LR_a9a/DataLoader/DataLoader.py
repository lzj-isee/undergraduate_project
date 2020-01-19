import torch
import numpy as np
from torch.utils.data import TensorDataset
from torch.utils.data import DataLoader, BatchSampler, RandomSampler


def Load_DataSet(batchSize):
    train_features=torch.Tensor(np.load('./DataSet/train_features.npy'))
    train_labels=torch.Tensor(np.load('./DataSet/train_labels.npy').reshape(-1))
    test_features=torch.Tensor(np.load('./DataSet/test_features.npy'))
    test_labels=torch.Tensor(np.load('./DataSet/test_labels.npy').reshape(-1))
    train_set=TensorDataset(train_features,train_labels)
    test_set=TensorDataset(test_features,test_labels)
    train_loader=DataLoader(
        train_set,
        num_workers=4,
        batch_sampler=BatchSampler(RandomSampler(train_set,replacement=True),batch_size=batchSize,drop_last=True))
    full_train_loader=DataLoader(
        train_set,
        num_workers=4,
        shuffle=True,
        batch_size=1000,
        drop_last=False)
    test_loader=DataLoader(
        test_set,
        shuffle=False,
        batch_size=1000,
        num_workers=4)
    return train_set,train_loader,full_train_loader,test_set,test_loader
