import random
def Unicode():
    val = random.randint(0x4e00, 0x9fbf)
    return chr(val)
a=[]
for i in range(1000000):
   a.append(Unicode()+Unicode()+Unicode()+Unicode()+Unicode()+Unicode()+'\n')
with open('keywords','w',encoding='utf-8') as f:
    f.writelines(a)