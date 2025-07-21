import numpy as np



def AND(x1,x2):
    x = np.array([x1, x2])
    w = np.array([0.5, 0.5])
    b = -0.7
    tmp = np.sum(x*w) + b
    if tmp <= 0:
        return 0
    else:
        return 1


def NAND(x1,x2):
    x = np.array([x1, x2])
    w = np.array([0.5, 0.5])
    b = -0.7
    tmp = np.sum(x*w) + b
    if tmp < 0:
        return 1
    else:
        return 0


def OR(x1,x2):
    x = np.array(x1, x2)
    w = np.array([0.5, 0.5])
    b = -0.2
    tmp = np.sum(x*w) + b
    if tmp <= 0:
        return 0
    else:
        return 1

def XOR(x1,x2):
    s1 = NAND(x1,x2)
    s2 = OR(x1,x2)
    y = AND(s1,s2)
    return y

if __name__ == '__main__':

    x = np.array([0, 1])
    w = np.array([0.5, 0.5])
    b = -0.7
    print(x*w)
    print(np.sum(x*w))
    print(np.sum(x*w) + b)
