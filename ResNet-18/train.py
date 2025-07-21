import copy
import matplotlib.pyplot as plt
import time

import pandas as pd
import torch
from torchvision.datasets import FashionMNIST
from torchvision import transforms
import torch.utils.data as Data
import numpy
from model import ResNet18 , Residual
import torch.nn as nn

#数据加载处理
def train_val_data_process():
    #加载数据
    train_data = FashionMNIST(root='./data',
                              train=True,
                              download=True,
                              transform=transforms.Compose([transforms.Resize(224),
                                                            transforms.ToTensor()]))

    #数据分割
    train_data,val_data = Data.random_split(train_data,[round(0.8*len(train_data)),round(0.2*len(train_data))])

    #设置数据批次
    train_dataloader = Data.DataLoader(dataset=train_data,
                                       batch_size=16,
                                       shuffle=True,
                                       num_workers=0)

    val_dataloader = Data.DataLoader(dataset=val_data,
                                       batch_size=16,
                                       shuffle=True,
                                       num_workers=0)

    return train_dataloader,val_dataloader

def train_model_process(model,train_dataloader,val_dataloader,num_epochs):
    device = torch.device("cuda" if torch.cuda.is_available() else 'cpu')
    #定义优化器，使用Adam
    optimizer = torch.optim.Adam(model.parameters(),lr=0.001)
    #损失函数为交叉熵函数
    critertion = nn.CrossEntropyLoss()
    #将模型放入到训练设备
    model = model.to(device)
    #保存训练参数
    best_model_wts = copy.deepcopy(model.state_dict())

    #初始化参数
    #最高准确度
    best_acc = 0.0
    #训练集损失列表
    train_loss_all = []
    #验证集损失列表
    val_loss_all = []
    #训练集准确度列表
    train_acc_all = []
    #验证集准确度列表
    val_acc_all = []

    since = time.time()

    for epoch in range(num_epochs):
        print("Epoch {}/{}".format(epoch,num_epochs-1))
        print('-'*10)

        #初始化参数
        #训练集损失函数
        train_loss = 0.0
        #训练集准确度
        train_corrects = 0
        #验证集损失函数
        val_loss = 0.0
        #验证集准确度
        val_corrects = 0
        #训练集样本数量
        train_num = 0
        #验证集样本数量
        val_num = 0

        #对每个mini-batch训练和计算
        for step,(b_x,b_y) in enumerate(train_dataloader):
            #将特征放入训练设备中
            b_x = b_x.to(device)
            b_y = b_y.to(device)
            #将模型设置为训练模式
            model.train()

            #前向转播过程，输入为一个batch，输出为一个batch中对于的预测
            output = model(b_x)
            #查找每一行中最大值对于的行标
            pre_lab = torch.argmax(output,dim=1)
            #计算每个batch的loss值
            loss = critertion(output,b_y)
            #将梯度初始化为0
            optimizer.zero_grad()
            #反向传播计算
            loss.backward()
            #根据网络反向传播的梯度信息来更新网络的参数，以起到降低loss函数计算值的作用
            optimizer.step()
            #对损失函数进行累加  就是统计每个batch的loss
            train_loss += loss.item() * b_x.size(0)
            #如果预测正确，则准确度train_corrects加1
            train_corrects += torch.sum(pre_lab == b_y.data)
            #当前用于训练的样本数量  就是统计样本数量
            train_num += b_x.size(0)

        for step, (b_x, b_y) in enumerate(val_dataloader):
            # 将特征放入训练设备中
            b_x = b_x.to(device)
            b_y = b_y.to(device)
            # 将模型设置为训练模式
            model.eval()
            output = model(b_x)
            pre_lab = torch.argmax(output,dim=1)
            loss = critertion(output,b_y)
            # 对损失函数进行累加
            val_loss += loss.item() * b_x.size(0)
            # 如果预测正确，则准确度train_corrects加1
            val_corrects += torch.sum(pre_lab == b_y.data)
            # 当前用于训练的样本数量
            val_num += b_x.size(0)

        # 计算并保存每一次迭代的loss值和准确率
        train_loss_all.append(train_loss / train_num)
        train_acc_all.append(train_corrects.double().item()/train_num)
        #保存验证集的loss值
        val_loss_all.append(val_loss / val_num)
        val_acc_all.append(val_corrects.double().item()/val_num)

        print("{} train loss: {:.4f} train acc: {:.4f}".format(epoch,train_loss_all[-1],train_acc_all[-1]))
        print("{} val loss: {:.4f} val acc: {:.4f}".format(epoch,val_loss_all[-1],val_acc_all[-1]))

        if val_acc_all[-1] > best_acc:
            #更新最高准确度的值
            best_acc = val_acc_all[-1]
            #更新参数
            best_model_wts = copy.deepcopy(model.state_dict())
        #训练耗费时间
        time_use = time.time() - since
        print("训练和验证耗费的时间{:.0f}m{:.0f}s".format(time_use//60,time_use%60))


    #选择最优参数
    #加载最高准确率下的模型参数
    torch.save(best_model_wts,r'.\best_model.pth')

    train_process = pd.DataFrame(data={"epoch":range(num_epochs),
                                       "train_loss_all":train_loss_all,
                                       "train_acc_all": train_acc_all,
                                       "val_loss_all": val_loss_all,
                                       "val_acc_all": val_acc_all, })
    return train_process

def matplot_acc_loss(train_process):
    plt.figure(figsize=(12,4))
    plt.subplot(1,2,1)
    plt.plot(train_process["epoch"],train_process.train_loss_all,'ro-',label = "train loss")
    plt.plot(train_process["epoch"],train_process.val_loss_all,'bs-',label = "val loss")
    plt.legend()
    plt.xlabel("epoch")
    plt.ylabel("loss")

    plt.subplot(1, 2, 2)
    plt.plot(train_process["epoch"], train_process.train_acc_all, 'ro-', label="train acc")
    plt.plot(train_process["epoch"], train_process.val_acc_all, 'bs-', label="val acc")
    plt.legend()
    plt.xlabel("epoch")
    plt.ylabel("acc")
    plt.legend()
    plt.show()


if __name__ == '__main__':
    #将模型实例化
    ResNet18 = ResNet18(Residual)
    train_dataloader,val_dataloader = train_val_data_process()
    train_process = train_model_process(ResNet18, train_dataloader, val_dataloader, 20)
    matplot_acc_loss(train_process)