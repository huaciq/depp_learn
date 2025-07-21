import numpy as np
import matplotlib.pylab as plt
def step_function(x):
    y = x > 0
    return y.astype(np.int32)

def sigmoid(x):
    return 1/(1+np.exp(-x))

def ReLU(x):
    return np.maximum(0,x)


def softmax(a):
    c = np.max(a)  # 防止溢出
    exp_a = np.exp(a - c)
    sum_exp_a = np.sum(exp_a)
    y = exp_a / sum_exp_a
    return y


if __name__ == '__main__':
   """
    x = np.arange(-5.0, 5.0, 0.1)
    y = sigmoid(x)

    plt.plot(x, y)
    plt.ylim(-0.1, 1.1)
    plt.show()
    """

a = np.array([0.3, 2.9, 4.0])