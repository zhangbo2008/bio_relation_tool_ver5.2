import re
import  time
a=time.time()
tmp=open('output.txt',encoding='utf-8').readlines()
out=[]
for i in tmp:
     out+=re.findall('.{1}某',i)
print(set(out))


print(time.time()-a)



import regex
import  time
a=time.time()

print(regex.findall(r'(?:(?=\d)\d+\b|\w+)', '123abc',concurrent=True))

print(time.time()-a)