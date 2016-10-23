# import os,copy
#
#
# # if os.path.exists("cat33.jpg"):
# #     print("ok")
# #
# # print("post app".split("|"))
#
# try_path = copy.deepcopy("")
# split_path = "bb".split('/')
# #try_path.extend(split_path)
#
# print(try_path)
# # print(split_path)
# # print(try_path)
#


# a="苑昊".encode()
# print(type(a))
#
# b=a.decode()
# print(type(b))
# print(b)



import hashlib

md5 = hashlib.md5()
md5.update("abc".encode())
print(md5.hexdigest())


# print('t'.join("_") )
# print("s".split()[0])


# print("uuu\iii".split("\\"))


a=[1,22,33,55]

a.pop(-1)
a.pop(-1)
print(a)