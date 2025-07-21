import torch
import torch.utils.data as Data
from torchvision import transforms
from torchvision.datasets import FashionMNIST
from model import LeNte

def test_data_process():
    #加载数据
    test_data = FashionMNIST(root='./data',
                              train=False,
                              download=True,
                              transform=transforms.Compose([transforms.Resize(28),
                                                            transforms.ToTensor()]))

    #设置数据批次
    test_dataloader = Data.DataLoader(dataset=test_data,
                                       batch_size=1,
                                       shuffle=True,
                                       num_workers=0)

    return test_dataloader


def test_model_process(model,test_dataloader):
    device = torch.device("cuda" if torch.cuda.is_available() else 'cpu')
    # 将模型放入到训练设备
    model = model.to(device)

    #初始化参数
    test_corrects = 0.0
    test_num = 0
    #只进行前向传播计算，不计算梯度，节省内存
    with torch.no_grad():
        for test_data_x,test_data_y in test_dataloader:
            # 将特征放入训练设备中
            test_data_x = test_data_x.to(device)
            test_data_y = test_data_y.to(device)
            # 将模型设置为测试模式
            model.eval()
            #前向传播过程
            output = model(test_data_x)
            #查找每一行中最大值对于的行标
            pre_lab = torch.argmax(output,dim=1)
            # 如果预测正确，则准确度train_corrects加1
            test_corrects += torch.sum(pre_lab == test_data_y.data)
            # 当前用于训练的样本数量  就是统计样本数量
            test_num += test_data_x.size(0)


    #计算测试准确率
    test_acc = test_corrects.double().item() / test_num
    print("测试的准确率为:",test_acc)

if __name__ == '__main__':
    #加载模型
    model = LeNte()
    model.load_state_dict(torch.load('best_model.pth'))
    test_dataloader = test_data_process()
    test_model_process(model,test_dataloader)

    #模型推理
    classes = ['T-shirt','Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
    device = torch.device("cuda" if torch.cuda.is_available() else 'cpu')
    # 将模型放入到训练设备
    model = model.to(device)
    with torch.no_grad():
        for b_x,b_y in test_dataloader:
            b_x = b_x.to(device)
            b_y = b_y.to(device)

            #设置模型为验证模型
            model.eval()
            output = model(b_x)
            pre_lab = torch.argmax(output,dim=1)
            result = pre_lab.item()
            label = b_y.item()
            print("预测值：",classes[result],"------","真实值：",classes[label])
