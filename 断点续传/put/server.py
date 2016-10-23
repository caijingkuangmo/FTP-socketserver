
import socket
import os

BASE_DIR=os.path.dirname(os.path.abspath(__file__))

home=os.path.join(BASE_DIR,"home/yuan")
ip_port=("127.0.0.1",8998)
sk=socket.socket()
sk.bind(ip_port)
sk.listen(5)

while True:
    print("waiting ....")
    conn,addr=sk.accept()
    conn.sendall(bytes("欢迎登录","utf8"))
    flag=True
    while flag:
        client_bytes=conn.recv(1024)
        client_str=str(client_bytes,"utf8")

        func,file_name,file_byte_size,target_pat=client_str.split("|",3)
        file_byte_size=int(file_byte_size)
        path=os.path.join(home,file_name)

        has_received=0

        if os.path.exists(path):
            conn.sendall(bytes("2003","utf8"))
            is_continue=str(conn.recv(1024),"utf8")
            if is_continue=="2004":
                has_file_size=os.stat(path).st_size
                conn.sendall(bytes(str(has_file_size),"utf8"))
                has_received+=has_file_size
                f=open(path,"ab")
            else:
                f=open(path,"wb")
        else:
            conn.sendall(bytes("2002","utf8"))
            f=open(path,"wb")

        while has_received<file_byte_size:
            try:
                data=conn.recv(1024)
                if not data:
                    raise Exception
            except Exception:
                flag=False
                break

            f.write(data)
            has_received+=len(data)
        print("ending")
        f.close()

























