import numpy as np

def euclidean_pose_distance(pa, pb):
    d = 0.0
    n = 0.0
    for i in range(len(pa)/2):
        if pa[2*i] >= 0 and pa[2*i+1] >= 0 and pb[2*i] >= 0 and pb[2*i+1] >= 0:
            d += np.sqrt(np.sum((pa[2*i:2*i+2] - pb[2*i:2*i+2])**2))
            n += 1.0
    if n != 0:
        return d/n
    else:
        return 10000

def cost_matrix(pa,pb,d):
    c = np.zeros((pa.shape[0],pb.shape[0]))
    for i in range(pa.shape[0]):
        for j in range(pb.shape[0]):
            c[i,j] = d(pa[i,:], pb[j,:])
    return squarify(c,0.0)

def squarify(M,val):
    (a,b)=M.shape
    if a>b:
        padding=((0,0),(0,a-b))
    else:
        padding=((0,b-a),(0,0))
    return np.pad(M,padding,mode='constant',constant_values=val)
