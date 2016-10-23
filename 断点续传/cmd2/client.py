import socket
ip_port=("127.0.0.1",9998)

sk=socket.socket()
sk.connect(ip_port)
print("客户端启动...")

print(str(sk.recv(1024),"utf8"))

while True:
    inp=input("please input:").strip()

    if inp.startswith("cmd"):

        sk.sendall(bytes(inp,"utf8"))
        basic_info_bytes=sk.recv(1024)
        print(str(basic_info_bytes,"utf8"))


        result_length=int(str(basic_info_bytes,"utf8").split("|")[1])

        print(result_length)
        has_received=0
        content_bytes=bytes()
        while has_received<result_length:
            fetch_bytes=sk.recv(1024)
            has_received+=len(fetch_bytes)
            content_bytes+=fetch_bytes
        cmd_result=str(content_bytes,"utf8")
        print(cmd_result)

sk.close()

