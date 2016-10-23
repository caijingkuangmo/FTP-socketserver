import subprocess

ret = subprocess.getoutput('arp')
ret = bytes(ret, encoding='gbk')
print(len(ret))
print(type(ret))

# import os
# os.system('arp')