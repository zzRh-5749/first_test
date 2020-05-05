#读取数据
import pandas as pd
import numpy as np
data=pd.read_csv('D:\\ke\\广告检测中的流量作弊识别\\data\\case_data.csv',engine='python')
data=data.iloc[:,1:]
data.columns=['记录序号','相对日期','cookie值','IP地址','idfa值','imei值','android值','openudid值','mac值','时间戳','项目ID','创意ID','设备OS版本信息','机型','app key信息','app name信息','广告位信息','浏览器信息','媒体id信息','OS类型标记','cookie生成时间','作弊标签']
#temp=pd.DataFrame()
#temp['null']=data.isnull().sum()
data1=data.loc[:,['记录序号','相对日期','cookie值','IP地址','时间戳','项目ID','创意ID','广告位信息','浏览器信息','媒体id信息','cookie生成时间','作弊标签']]
#data2=data.loc[:,['idfa值','imei值','android值','openudid值']]
#data5=pd.DataFrame(columns=['IOS','Android'])
#data5.iloc[:,0]=data2.iloc[:,0].combine_first(data2.iloc[:,3])
#data5.iloc[:,1]=data2.iloc[:,1].combine_first(data2.iloc[:,2])
#data5.iloc[data5[data5.iloc[:,0].notnull()].index,0]=1
#data5.iloc[data5[data5.iloc[:,0].isnull()].index,0]=0
#data5.iloc[data5[data5.iloc[:,1].notnull()].index,1]=2
#data5.iloc[data5[data5.iloc[:,1].isnull()].index,1]=0
#转化成数值型
from sklearn.preprocessing import LabelEncoder
for i in range(4):
    data1.iloc[:, i] = LabelEncoder().fit_transform(data1.iloc[:, i])
#排序
data1.sort_values(by = '时间戳',axis = 0,ascending = False)
#第一种作弊方式
lis=np.linspace(0,604800,169,endpoint=True)
data1.index=data1["cookie值"].map(str) + data1['IP地址'].map(str)
data1['A1']=0
for i in range(len(lis)):
    data11=data1[((data1.时间戳>=lis[i])&(data1.时间戳<=lis[i+1]))]
    data11["newColumn"] = data11["cookie值"].map(str) + data11['IP地址'].map(str)
    data1_2=data11["newColumn"].value_counts()
    data11.index=data11["newColumn"]
    data1.loc[data1_2.index,'A1']=data1_2[data1_2.index]
data1.index=range(len(data1))
#第二种作弊方式
data1['A2']=0
data1.index=data1.IP地址
for i in range(len(lis)):
    data11 = data1[((data1.时间戳 >= lis[i]) & (data1.时间戳 <= lis[i + 1]))]
    data2_2=data11["IP地址"].value_counts()
    data11.index=data11["IP地址"]
    data1.loc[data2_2.index,'A2']=data2_2[data2_2.index]
data1.index=range(len(data1))
#第三种作弊方式
data1['A3']=0
import re
data3=data.IP地址
data3_1=data3.apply(lambda x:re.findall('[0-9]{1,3}[\.]',str(x)))
data3_2=[]
for i in range(len(data3_1)):
    data3_2.append(data3_1[i][0]+data3_1[i][1])
data3_3=pd.Series(data3_2)
data3_4=data3_3.value_counts()
data1.index=data3_2
data1.loc[data3_4.index,'A3']=data3_4[data3_4.index]

#第四种作弊方式
data1['A4']=0
import re
data3=data.IP地址
data3_1=data3.apply(lambda x:re.findall('[0-9]{1,3}[\.]',str(x)))
data4_2=[]
for i in range(len(data3_1)):
    data4_2.append(data3_1[i][0]+data3_1[i][1]+data3_1[i][2])
data4_3=pd.Series(data4_2)
data4_4=data4_3.value_counts()
data1.index=data4_2
data1.loc[data4_4.index,'A4']=data4_4[data4_4.index]
data1.index=range(len(data1))
#决策树
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report,confusion_matrix,f1_score
x_train,x_test,y_train,y_test=train_test_split(data1.iloc[:,[4,-4,-3,-2,-1]],data1.iloc[:,-5],test_size=0.2,random_state=123)
dec=DecisionTreeClassifier().fit(x_train,y_train)
y_pre=dec.predict(x_test)
classification_report(y_test,y_pre)
confusion_matrix(y_test,y_pre)
f1_score(y_test,y_pre)