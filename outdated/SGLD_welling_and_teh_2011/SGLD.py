import numpy as np 
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D
import math
import seaborn as sns

def posterior_calculate(theta_list_1,theta_list_2,x_list):
    '''
    计算后验
    theta_list_1: theta_1的扫描点
    theta_list_2: theta_2的扫描点
    x_list: 生成的随机点
    '''
    posterior=np.ones((len(theta_list_1),len(theta_list_2)),dtype=float)
    for i in range(len(theta_list_1)):
        for j in range(len(theta_list_2)):
            #算先验
            posterior[i][j]=math.exp(-(theta_list_1[i]**2)/(2*sigma_1**2))/(math.sqrt(2*math.pi)*sigma_1)
            posterior[i][j]=posterior[i][j]*math.exp(-(theta_list_2[j]**2)/(2*sigma_2**2))/(math.sqrt(2*math.pi)*sigma_2)
            for  k in range(len(x_list)):
                #算极大似然
                posterior[i][j]=posterior[i][j]*math.exp(-((x_list[k]-theta_list_1[i]-0.5*theta_list_2[j])**2)/(sigma_x**2))\
                    /math.sqrt(2*math.pi*(0.5*(sigma_x**2)))
    Sum=sum(sum(posterior))
    for i in range(len(theta_list_1)):
        for j in range(len(theta_list_2)):
            posterior[i][j]=posterior[i][j]/Sum
    return posterior

def posterior_image_surface(theta_list_1,theta_list_2,x_list):
    '''
    画出后验的三维surface图
    '''
    posterior=posterior_calculate(theta_list_1,theta_list_2,x_list)
    X,Y=np.meshgrid(theta_list_1,theta_list_2)
    ax=plt.subplot(111,projection='3d')
    ax.plot_surface(X,Y,np.transpose(posterior),cmap='rainbow')

def posterior_image_contourf(theta_list_1,theta_list_2,x_list,plot_levels):
    '''
    画出后验的等高线图
    '''
    posterior=posterior_calculate(theta_list_1,theta_list_2,x_list)
    X,Y=np.meshgrid(theta_list_1,theta_list_2)
    plt.contourf(X,Y,np.transpose(posterior),plot_levels+2,alpha=0.75)
if __name__=='__main__':
    '''参数设置'''
    sigma_1=math.sqrt(10)
    sigma_2=math.sqrt(1)
    sigma_x=math.sqrt(2)
    max_iteration=10000
    theta_1=0
    theta_2=1
    x_num=100
    plot_levels=9 #核密度估计的层数
    '''设置步长---epsilon=a*(b+t)**(-gamma)'''
    gamma=0.55
    a=0.2
    b=30
    '''生成数据点'''
    x_list=(np.random.normal(theta_1,sigma_x,x_num)\
        +np.random.normal(theta_1+theta_2,sigma_x,x_num))/2
    '''生成后验分布的网格扫描点'''
    theta_list_1=np.linspace(-1.5,2.5,100)
    theta_list_2=np.linspace(-3,3,99)
    '''计算后验网格矩阵作为参考'''
    posterior=posterior_calculate(theta_list_1,theta_list_2,x_list)

    '''
    Stochastic Gradient Langevin Dynamics
    '''
    theta_iteration_1=[0] #thate迭代值，这里可以设置初始值
    theta_iteration_2=[0]
    gredient=[0,0]
    for i in range(max_iteration):
        epsilon=a*((b+i+1)**(-gamma))
        gredient[0]=-theta_iteration_1[i]/(2*sigma_1**2)
        gredient[1]=-theta_iteration_2[i]/(2*sigma_2**2)
        for j in range(x_num):#这里要改成随机梯度
            gredient[0]=gredient[0]-2*(theta_iteration_1[i]+0.5*theta_iteration_2[i]-x_list[j])/(sigma_x**2)
            gredient[1]=gredient[1]-(theta_iteration_1[i]+0.5*theta_iteration_2[i]-x_list[j])/(sigma_x**2)
        temp1=theta_iteration_1[i]+epsilon*gredient[0]/2+np.random.normal(0,math.sqrt(epsilon),1)
        temp2=theta_iteration_2[i]+epsilon*gredient[1]/2+np.random.normal(0,math.sqrt(epsilon),1)
        theta_iteration_1.append(temp1)
        theta_iteration_2.append(temp2)
    print("max_epsilon:%f, min_epsilon:%f"%(a*((b+1)**(-gamma)),a*((b+max_iteration)**(-gamma))))
    X,Y=np.meshgrid(theta_list_1,theta_list_2)
    plt.contour(X,Y,np.transpose(posterior),plot_levels-2)
    plt.scatter(theta_iteration_1,theta_iteration_2,alpha=0.02)
    sns.jointplot(theta_iteration_1,theta_iteration_2,data=None,kind='kde',space=0,xlim=[-1.5,2.5],ylim=[-3,3],shade_lowest=False,n_levels=plot_levels)
    plt.show()
