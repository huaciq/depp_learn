from torchvision.datasets import FashionMNIST
from torchvision import transforms
import torch.utils.data as Data
import numpy
import matplotlib.pyplot as plt

#加载数据
train_data = FashionMNIST(root='./data',
                          train=True,
                          download=True,
                          transform=transforms.Compose([transforms.Resize(224),
                                                        transforms.ToTensor()]))

#处理数据
train_loader = Data.DataLoader(dataset=train_data,
                               batch_size=64,
                               shuffle=True,
                               num_workers=0)


#获得一个batch的数据
for step, (b_x, b_y) in enumerate(train_loader):
    if step > 0:
        break  # 仅处理第一个Batch后退出循环
    batch_x = b_x.squeeze().numpy()  # 移除单维度并转为Numpy
    batch_y = b_y.numpy() #将张量转为numpy数组
    class_label = train_data.classes  # 获取类别标签
    print("The size of batch in train data:", batch_x.shape)


#可视化一个batch图像
plt.figure(figsize=(12, 5))
for ii in range(len(batch_y)):  # 使用range代替np.arange更规范
    plt.subplot(4, 16, ii + 1)  # 修正参数语法
    # 若为RGB图像，需调整通道顺序：
    # plt.imshow(batch_x[ii].transpose(1, 2, 0))
    plt.imshow(batch_x[ii], cmap=plt.cm.gray)  # 灰度图保持原状
    plt.title(class_label[batch_y[ii]], size=10)
    plt.axis("off")
plt.subplots_adjust(wspace=0.05)  # 调整子图间距
plt.show()