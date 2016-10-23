import socket
import re,os,sys
ip_port=("127.0.0.1",8898)
sk=socket.socket()
sk.connect(ip_port)

print("客户端启动....")
print(str(sk.recv(1024),"utf8"))


def bar(num=1, sum=100):

    rate = float(num) / float(sum)
    rate_num = int(rate * 100)
    temp = '\r%d %%' % (rate_num, )
    sys.stdout.write(temp)
    sys.stdout.flush()

while True:
    inp=input("please input:")
    if inp.startswith("post"):
        method,file_path=inp.split("|",1)

        local_path,target_path=re.split("\s*",file_path,1)
        file_byte_size=os.stat(local_path).st_size
        file_name=os.path.basename(local_path)

        post_info="post|%s|%s|%s"%(file_byte_size,file_name,target_path)
        sk.sendall(bytes(post_info,"utf8"))
        result_exist=str(sk.recv(1024),"utf8")
        has_sent=0
        if result_exist=="2003":
            inp=input("文件已经存在，是否续传？Y/N").strip()
            if inp.upper()=="Y":
                sk.sendall(bytes("2004","utf8"))
                result_continue_pos=str(sk.recv(1024),"utf8")
                has_sent=int(result_continue_pos)
            else:
                sk.sendall(bytes("2005","utf8"))

        file_obj=open(local_path,"rb")
        file_obj.seek(has_sent)

        while has_sent<file_byte_size:
            data=file_obj.read(1024)
            sk.sendall(data)
            has_sent+=len(data)
            bar(has_sent,file_byte_size)
        file_obj.close()
        print("上传成功")










