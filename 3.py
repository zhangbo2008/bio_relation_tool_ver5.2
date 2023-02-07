import re


#用于大量匹配这种来标注.
a=re.findall('.{1}某','sdfsadf张某,李某,sdfsdfasfasd王某他们杀人了')
a=re.findall('.{2,3}研究所','内蒙古研究所,  北京研究所, 新疆研究所')


print(a)