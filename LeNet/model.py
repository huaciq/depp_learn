import torch
from torch import nn
from torchsummary import summary


class LeNte(nn.Module):
    #相当定义一些基本操作，卷积池化激活等
    def __init__(self):    #固定格式，做初始化
        super().__init__()
        self.c1 = nn.Conv2d(in_channels=1,kernel_size=5,padding=2,out_channels=6)
        self.sig = nn.Sigmoid()
        self.s2 = nn.AvgPool2d(kernel_size=2,stride=2)
        self.c3 = nn.Conv2d(in_channels=6,out_channels=16,kernel_size=5)
        self.s4 = nn.AvgPool2d(kernel_size=2,stride=2)
        self.flatten = nn.Flatten()
        self.f5 = nn.Linear(400,120)
        self.f6 = nn.Linear(120,84)
        self.f7 = nn.Linear(84,10)

    #定义前向传播操作
    def forward(self,x):
        x = self.sig(self.c1(x))
        x = self.s2(x)
        x = self.sig(self.c3(x))
        x = self.s4(x)
        x = self.flatten(x)
        x = self.f5(x)
        x = self.f6(x)
        x = self.f7(x)
        return x

if __name__ == '__main__':
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    #模型实例化
    model = LeNte().to(device)
    print(summary(model,(1,28,28)))