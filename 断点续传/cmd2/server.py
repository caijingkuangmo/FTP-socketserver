import socketserver
import subprocess

class Myserver(socketserver.BaseRequestHandler):
    def handle(self):
        while True:
            conn=self.request
            conn.sendall(bytes("欢迎登录","utf8"))
            while True:
                client_bytes=conn.recv(1024)
                if not client_bytes:break
                client_str=str(client_bytes,"utf8")
                print(client_str)
                func,command=client_str.split("|",1)

                result_str=subprocess.getoutput(command)
                result_bytes = bytes(result_str,encoding='utf8')
                info_str="info|%d"%len(result_bytes)
                conn.sendall(bytes(info_str,"utf8"))

                conn.sendall(result_bytes)
            conn.close()









if __name__=="__main__":
    server=socketserver.ThreadingTCPServer(("127.0.0.1",9998),Myserver)
    server.serve_forever()