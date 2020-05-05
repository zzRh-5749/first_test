import pandas as pd
import re

data=pd.read_csv('F:\Python_Programe\pinglun13.csv',encoding='gbk')   #将导入需要处理的信息
data=data.评论  #提取评论
len(data)

#数据预处理
data=data.apply(lambda x:re.sub(r'\\n','',str(x)))       #将换行符换成空格
data=data.apply(lambda x:re.sub('&[a-z]{1,10};','',str(x)))   #&hellip;表情符号删除:以&符号开始,以;结束
len(data)

##使用jieba模块对中文语句（将一句话分成多个词语）进行分词  lcut直接返回 list
import jieba
data_cut=data.apply(lambda x:jieba.lcut(x))

##对停用词进行相关处理
stop=pd.read_csv('F:\Python_Programe\stoplist.txt',header=None,encoding='utf-8',sep='song')
len(stop)
stop.drop_duplicates(inplace=True)   # 去除stop中重复的信息
stop=[' ','\u3000']+list(stop[0])
len(stop)
#将停用词表中的否定词和程度副词去除
degree=pd.read_csv('F:\Python_Programe\degree.csv',engine='python',encoding='utf-8') #导入程度副词表
degree.columns=['term']#把列名换成term
degree['score']=degree.index #增加一个score列，里面是对应行索引列的内容
degree.index=list(range(0,len(degree)))#将索引列换成数字索引
no=pd.read_csv('F:\Python_Programe\not.csv',engine='python',encoding='utf-8')#导入否定词表
no['score']=-999  #增加一个score列，每一行的值都是-999
dic=pd.concat([degree,no],axis=0)  #将程度副词表和否定词表结合成一个表（dic）

#从停用词中删除程度副词和否定词
for i in dic.term:
     if i in stop:
        stop.remove(i)
data_after=data_cut.apply(lambda x:[i for i in x if i not in stop])  #去掉分词中的停用词



#词频
import pandas as pd
import re
def cipin(x,n=10):
     x=data_after
     temp=[' '.join(i) for i in x]
     temp1=' '.join(temp)
     temp2=pd.Series(temp1.split())
     num=temp2.value_counts() #统计每个名词的数量
     return (num[num>n]) #只有一个词出现10次以上才会统计
cut_num=cipin(data_after)
num=cipin(data_after)  #调用cipin函数生成统计表


import cv2
from wordcloud import WordCloud  #用第三方库wordcloud生成词云
import matplotlib.pyplot as plt    #采用matplotlib中的plt作图
plt.rcParams['font.sans-serif'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False
back_pic = cv2.imread("F:\Python_Programe\timg.jpg")  # 设置词云形状图片
wc = WordCloud(font_path='simkai.ttf',  background_color="white", max_words=1000,mask=back_pic,max_font_size=200,random_state=42)
gar_wordcloud = wc.fit_words(num[:400])  # 显示出现num词频统计表中到400的词语
plt.figure(figsize=(16, 8))
plt.imshow(gar_wordcloud)
plt.title('DW手表评价')
plt.axis('off')
plt.show()



#情感倾向分析
#导入情感词表(header换成None，数字索引)
feel=pd.read_table('F:\Python_Programe\BosonNLP_sentiment_score.txt',sep=' ',header=None,engine='python',encoding='utf-8')
feel.columns=['word1','score1']  #将列名换成word1和score1
#评分
#分词后的结果,转为Series的格式
temp=' '.join([' '.join(x) for x in data_after])
new_data=pd.Series(temp.split())      ##将字符串进行分割
len(new_data)
ID=[]
for i in data_after.index:   #由于分词后每一行有多个词，所以要把每一行这多个词的个数作作为id中的数，以至于计算新数据的索引长度
    ID.extend([i]*len(data_after[i]))   #extend将括号内的数值加到ID这个列表中
new_data.index=ID    #把新数据的索引换成ID用来索引
len(new_data)   #查看新数据长度
new_data=pd.DataFrame(new_data) #把新数据换成DataFrame
new_data.columns=['word']  #将新数据的列名改成word

##把否定词表,评分表,以及分词结果合并
temp=pd.merge(new_data,feel,how='left',left_on='word',right_on='word1') #将新分词数据与评分表合并
ndata=pd.merge(temp,dic,how='left',left_on='word',right_on='term')     #将上述表和dic表（程度副词和否定词表合并）
ndata.index=ID
del ndata['word1'],ndata['term']  #删除表中的word1和term列
index_dic=list(set(ndata[ndata['score'].isnull()==False].index))   #找出包含否定词,程度副词的Index
index_nor =list(set([i for i in ndata.index if i not in index_dic])) #找出不包含否定词,程度副词的Index
new_score = pd.DataFrame(index=list(set(ndata.index)))  #对不含否定词,程度词的评论进行评分求和
new_score['score'] = 0  ## 储存我们情感总分
for i in index_nor:
    new_score.loc[i,'score'] = ndata.loc[0,'score1'].sum()     #计算情感总分

# 对含有否定词、程度词的评论进行情感分值的调整
for i in index_dic:
    temp = ndata.loc[i]
    if len(temp.word) > 1:
        temp.index = range(len(temp))
        # 否定词 -999
        #1 双重否定表肯定；2 否定词在句末；3 否定词后面是词语，词语情感反转
        a = [x for x in temp.index if temp.loc[x,'score'] == -999]
        for k in a:
            if k == len(temp) - 1:                #2 否定词在句末
                temp.loc[k,'score1'] = 0
            elif temp.loc[k+1,'score'] == -999:  #1 双重否定表肯定；
                temp.loc[k,'score1'] = 0
                temp.loc[k+1,'score1'] = 0
                a.remove(k+1)
            else:
                temp.loc[k,'score1'] = 0    #3 否定词后面是词语，词语情感反转
                temp.loc[k+1,'score1'] = (-1)*temp.loc[k+1,'score1']
        # 程度词-50、-200、-400%10==0;程度词在句末；不在句末
        b = [i for i in range(len(temp)) if temp.loc[i,'score']%10 == 0]
        for k in b:
            if k == len(temp) -1:
                temp.loc[k,'score1'] = 0
            else:
                temp.loc[k+1, 'score1'] = temp.loc[k+1,'score1']*temp.loc[k, 'score']/(-100)
                temp.loc[k, 'score1'] = 0
    new_score.loc[i,'score'] = temp.score1.sum()


new_score['score'].sort_values(ascending=False)
len(data_after)
data_after[6057]

# 根据new_score的分数将评论划分为正面评论及负面评论
index_pos = [i for i in new_score.index if new_score.loc[0,'score'] > 0] #将分数大于0的找出设置为正面评论
pos = data_after[index_pos]    ##正面评论

index_neg = [i for i in new_score.index if new_score.loc[i,'score'] < 0]  #将分数小于0的找出设置为正面评论
neg = data_after[index_neg]    ##负面评论


##根据正面评论绘制词云
num=[]
[num.extend(i) for i in pos]
num=pd.Series(num).value_counts()
import cv2
from wordcloud import WordCloud  #用第三方库wordcloud生成词云
import matplotlib.pyplot as plt    #采用matplotlib中的plt作图
plt.rcParams['font.sans-serif'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False     #显示负号
back_pic = cv2.imread("F:\Python_Programe\timg.jpg")  # 设置词云形状
wc = WordCloud(font_path='simkai.ttf',  background_color="white", max_words=1000,mask=back_pic,max_font_size=200,random_state=42)
gar_wordcloud = wc.fit_words(num[:400])  # 显示出现num词频统计表中到400的词语
plt.figure(figsize=(16, 8))  #宽和高
plt.imshow(gar_wordcloud)  #显示一个二维表
plt.title('DW正面手表评价')
plt.axis('off')
plt.show()

