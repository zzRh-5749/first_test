import re

'''
re.match 函数
尝试从字符串的起始位置匹配一个模式
match(pattern,string flags=0)
patter 匹配的正则表达式
string 匹配的字符串
flags 标志位，用于控制正则表达式的匹配方式 值如下
re.I  忽略大小写
re.L  做本地户识别
re.M  多行匹配，影响^和$
re.S  是.匹配包括换行符在内的所有字符
re.U  根据Unicode字符集解析字符 影响\w \W \b \B
re.X  使我们以更灵活的方式理解正则表达式
'''

'''
s = "www.baidu.com"
t = re.match("www",s,flags=0)
print(t)
'''

"""
re.search()

re.findall 
"""


