import torch
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
import numpy as np

transforms = transforms.Compose([
    transforms.ToTensor()
])

print("\n正在下载和加载 MNIST 数据集...")
train_dataset = torchvision.datasets.MNIST(root='/.data',train=True,transform=transforms,download=True)
test_dataset = torchvision.datasets.MNIST(root='/.data',train=False,transform=transforms,download=True)

print("数据集加载完成！")

print("\n--- 数据集信息 ---")
print(f"训练样本数量：{len(train_dataset)}")
print(f"测试样本数量：{len(test_dataset)}")

print("单个样本信息")
first_image, first_label = train_dataset[0]

print(f"图片张量形状：{first_image.shape}")
print(f"图像的数据类型：{first_image.dtype}")
print(f"标签信息：{first_label}")

train_loader = torch.utils.data.DataLoader(
    dataset=train_dataset,
    batch_size=32,
    shuffle=True
)

test_loader = torch.utils.data.DataLoader(
    dataset=test_dataset,
    batch_size=64,
    shuffle=False
)

images, labels = next(iter(train_loader))

print("\n--- DataLoader 批次信息 ---")
print(f"一个批次的图像张量形状: {images.shape}")
# 输出: torch.Size([64, 1, 28, 28]) -> [BatchSize, Channel, Height, Width]
print(f"一个批次的标签张量形状: {labels.shape}")
# 输出: torch.Size([64])




