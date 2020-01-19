import numpy as np
import matplotlib.pyplot as plt
import os

path='./result/SRM_HMC/'
file_names=list(os.listdir(path))
for i,file_name in enumerate(file_names):
    if file_name[len(file_name)-3:len(file_name)] != 'npy':
        file_names.pop(i)

for file_name in file_names:
    data=np.load(path+file_name)[0]
    plt.plot(data,label=file_name)
plt.legend()
plt.ylim([0.32,0.4])
plt.show()