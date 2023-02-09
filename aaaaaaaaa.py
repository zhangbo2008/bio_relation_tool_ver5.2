import re
a = "123abc456啊啊啊啊啊啊啊啊abc456123abc456"
print(re.search("([0-9]*)([a-z]*)([0-9]*)",a).group(0))   #123abc456,返回整体
print(re.search("([0-9]*)([a-z]*)([0-9]*)",a).group(1)) #123
print(re.search("([0-9]*)([a-z]*)([0-9]*)",a).group(2)) #abc
print(re.search("([0-9]*)([a-z]*)([0-9]*)",a).group(3))  #456
print(re.findall("([0-9]*)([a-z]*)([0-9]*)",a))  #456




print('----------------------')

str1 = "123@qqqq.comaaa@163.combbb@126.comasdf111@asdfcom  asdf111@126126asdfcom"

print(re.findall(r"\w+@(qq|163|126)(qq|163|126)\.com", str1))
print(re.findall(r"\w+@qq|163|126\.com", str1))
print(re.findall(r"\w+@{qq|163|126}\.com", str1))
print(re.findall(r"\w+@(?:qq|163|126)\.com",str1))
print(re.findall(r"@(?:126)*",str1))
print(re.findall(r"@(126)*",str1))

str1='2015-8-7'

print(re.findall(r"-(\d+)-",'2015-8-7')) # 8






