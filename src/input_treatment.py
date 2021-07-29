import numpy as np


def get_input():
    n, m = input().split()
    c = input().split()
    a = []
    b = []
    for i in range(int(n)):
        restrictions = input().split()
        a.append(restrictions[0:len(restrictions)-1])
        b.append(restrictions[len(restrictions)-1])
    return int(n), int(m), np.array(c).astype(np.float), np.array(a).astype(np.float), np.array(b).astype(np.float)