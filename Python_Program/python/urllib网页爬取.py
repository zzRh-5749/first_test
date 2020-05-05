import urllib.request


#向指定的URL地址发起请求，并返回服务器响应的数据（文件的对象）

response=urllib.request.urlopen("http://www.baidu.com")

data=response.read().decode("utf-8");
print(data)

data=response.readlines()

##print(type(data))
##print(len(data))