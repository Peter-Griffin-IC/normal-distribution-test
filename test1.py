import pandas as pd
import numpy as np
from scipy.stats import norm
from scipy.stats import chi2

t=[]
s=0
df = pd.read_excel("5.xlsx", index_col=0)#读取数据，创造数据矩阵t
list_values = df.values.tolist()
for item in list_values:
    t.append([item[0]])
k=np.sum(t)/len(t)                       #求均值
for i in range(len(t)):                  #求方差
    s=s+(t[i]-k)**2/len(t)
s=float(s[0])
n=5                                      #划分的区间的个数
star=8                                   #所划分的第一个区间的下界
interval=1                               #区间长度

#统计落在各个区间的频数
b=[x for x in range(star,star+1+(n-2)*interval,interval)]
c=[10**5]#取一个足够大的数字代表正无穷
tt = np.array(t)
ttt=tt.flatten().tolist()
if star==0:
    inte=np.hstack((b,c))
    nf=pd.cut(ttt,bins=inte)
else:
    a=[0]
    inte=np.hstack((a,b,c))
    nf=pd.cut(ttt, bins=inte)
values = nf.value_counts().values        #统计出的频数矩阵


#计算p的估计值
q=[]
for y in range(n-1):
    if y==0:
        l = norm.cdf((star + y*interval - k) / np.sqrt(s))
    else:
        l = norm.cdf((star +y*interval-k)/np.sqrt(s))- norm.cdf((star +y*interval-1-k)/np.sqrt(s))
    q.append(l)
q.append(1-np.sum(q))

#计算出检验统计量的样本值
sample=0
for y in range(n):
    sample= sample + ((values[y]-len(t)*q[y])**2)/(len(t)*q[y])

#进行卡方检验
np=n-2-1                                     #自由度
alpha=0.05                               #显著水平a
right_quarti=chi2.isf(q=alpha, df=np)    #计算单尾假设检验右分位点
ans=bool(sample < right_quarti)

print('均值估计值是：%f, 方差估计值是：%f' %(k,s))
print("p的估计值分别为:")
print(q)
print("检验统计量的样本值为:%4f"%sample)
print("正态分布检验结果:")
print(ans)
