import socket,os
ip_port=("127.0.0.1",8898)
sk=socket.socket()
sk.bind(ip_port)
sk.listen(5)
BASE_DIR=os.path.dirname(os.path.abspath(__file__))
home=os.path.join(BASE_DIR,"home/yuan")
REQUEST_CODE = {
    '1001': 'cmd info',
    '1002': 'cmd ack',
    '2001': 'post info',
    '2002': 'ACK（可以开始上传）',
    '2003': '文件已经存在',
    '2004': '续传',
    '2005': '不续传',
    '3001': 'get info',
    '3002': 'get ack',

}
while True:
    print("waiting connect")
    conn,addr=sk.accept()
    conn.sendall(bytes("欢迎登录...","utf8"))
    flag = True
    while flag:
        try:
            print("wait")
            client_bytes=conn.recv(1024)
            if not client_bytes:
                print('llllll')
                break
        except Exception:
            break
        else:
            client_str=str(client_bytes,"utf8")
            func,file_byte_size,filename,target_path=client_str.split("|",3)
            path=os.path.join(home,filename)

            has_received=0
            file_byte_size=int(file_byte_size)

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
                        raise  Exception('control c')
                except Exception as e:
                    flag = False
                    break
                f.write(data)
                has_received+=len(data)
            print("ending")
            f.close()



















