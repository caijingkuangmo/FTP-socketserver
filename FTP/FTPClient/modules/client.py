import os, sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

import socket
import json
import hashlib
import copy


class Client:

    def __init__(self, sys_argv):
        self.USER_HOME = '%s/var/users' % BASE_DIR
        self.args = sys_argv
        self.argv_parse()
        self.response_code = {
            "200": "pass user authentication",
            "201": "wrong username or password",
            "300": "ready to get file from server",
            "301": "ready to send to server",
            "302": "file doesn't exist on ftp server",
            "303": "storage is full",
            "601": "changed directory",
            "602": "failed to find directory",
            '2003': 'file exist',
            '2004': 'continue put',
        }
        self.handle()

    def help_msg(self):
        msg = '''
            -s ftp_server_addr
            -p ftp_server_port
        '''
        print(msg)

    def instruction_msg(self):
        msg = '''
            get ftp_file
            put local remote
            ls
            cd path
        '''
        print(msg)

    def argv_parse(self):
        if len(self.args) < 5:
            self.help_msg()
            sys.exit()
        else:
            mandatory_fields = ["-p", "-s"]
            for i in mandatory_fields:
                if i not in self.args:
                    self.help_msg()
                    sys.exit("")
            try:
                self.ftp_host = self.args[self.args.index("-s") + 1]
                self.ftp_port = int(self.args[self.args.index("-p") + 1])
            except (IndexError, ValueError):
                self.help_msg()
                sys.exit()

    def connect(self, host, port):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((host, port))
        except socket.error as e:
            sys.exit("Failed to connect server:%s" % e)

    def auth(self):
        retry_count = 0
        while retry_count < 3:
            username = input("Please enter your username:")
            if len(username) == 0: continue
            password = input("Please enter your password:")
            if len(password) == 0: continue
            md5 = hashlib.md5()
            md5.update(password.encode())
            auth_str = "user_auth|%s" % (json.dumps({"username": username, "password": md5.hexdigest()}))
            self.sock.send(auth_str.encode())
            server_response = self.sock.recv(1024).decode()
            response_code = self.get_response_code(server_response)
            if response_code == "200":
                self.login_user = username
                self.cwd = [""]
                try:
                    os.makedirs("%s/%s" % (self.USER_HOME, self.login_user))
                except OSError:
                    print("hhhh")
                    pass

                return True
            else:
                retry_count += 1
        else:
            sys.exit("Too many attemps")


    def get_response_code(self, response):
        response_code = response.split("|")
        code = response_code[1]
        return code

    def parse_instruction(self, user_input):
        user_input_to_list = user_input.split()
        func_str = user_input_to_list[0]
        if hasattr(self, 'instruction_' + func_str):
            return True, user_input_to_list
        else:
            return False, user_input_to_list

    def current_dir(self, cwd):
        return '/'.join(cwd) + '/'

    def interactive(self):
        self.logout_flag = False
        while self.logout_flag is not True:
            user_input = input("[%s]:%s" % (self.login_user, self.current_dir(self.cwd))).strip()
            if len(user_input) == 0: continue
            status, user_input_instructions = self.parse_instruction(user_input)
            if status is True:
                func = getattr(self, 'instruction_' + user_input_instructions[0])
                func(user_input_instructions)
            else:
                print("Invalid instruction.")

    def instruction_ls(self, instructions):
        self.sock.send(("ls|%s" % json.dumps({})).encode())
        server_response = self.sock.recv(1024)
        print(str(server_response,"gbk"))

    def instruction_dir(self, instructions):
        self.sock.send(("dir|%s" % json.dumps({})).encode())
        server_response = self.sock.recv(1024).decode()
        print(server_response)
        # server_response_json = json.loads(self.sock.recv(1024).decode())
        # print(server_response_json['result'])

    def instruction_cd(self, instructions):
        print("instr:",instructions)#instr: ['cd', 'animal']
        if len(instructions) == 1:
            # self.sock.send(("cd|%s" % json.dumps({"cwd": [""]})).encode())
            # self.sock.recv(1024)
            # self.cwd = [""]
            print("gg")
        elif len(instructions) == 2:
            path = instructions[1]
            if path.startswith('/'):
                try_path = path.split('/')
            else:
                # try_path = copy.deepcopy(self.cwd)
                try_path=self.cwd
                print("try_path",try_path)
                split_path = path.split('/')
                try_path.extend(split_path)
                print("try_path1",try_path)
            self.sock.send(("cd|%s" % json.dumps({"cwd": try_path})).encode())
            server_response = json.loads(self.sock.recv(1024).decode())
            if server_response['response'] == '601':
                print("self.cwd",server_response['cwd'])
                if server_response['cwd'][-1]=="..":
                    server_response['cwd'].pop(-1)
                    server_response['cwd'].pop(-1)



                self.cwd = server_response['cwd']
            elif server_response['response'] == '602':
                print("directory doesn't exist")

    def bar(self,num=1, sum=100):

        rate = float(num) / float(sum)
        rate_num = int(rate * 100)
        temp = '\r%d %%' % (rate_num, )
        sys.stdout.write(temp)
        sys.stdout.flush()

    def instruction_put(self, instructions):
        print("fff")
        if len(instructions) < 2:
            print("Please add the file path that you want to upload")
            return
        else:
            local_path = instructions[1]

            if os.path.exists(local_path):
                print("ooooooooooooooooooooo")
                file_name = os.path.basename(local_path)
                file_size = os.path.getsize(local_path)
                print(file_name,file_size)
                command_str = "file_put|%s" % (json.dumps({"file_name": file_name, "file_size": file_size}))
                self.sock.send(command_str.encode())
                ok=str(self.sock.recv(1024),"utf8")
                result_exist=str(self.sock.recv(1024),"utf8")
                print(result_exist)

                has_sent=0
                if result_exist=="2003":
                    inp=input("文件存在，是否续传？Y/N").strip()
                    if inp.upper()=="Y":
                        self.sock.sendall(bytes("2004","utf8"))
                        result_continue_pos=str(self.sock.recv(1024),"utf8")
                        print(result_continue_pos)
                        has_sent=int(result_continue_pos)

                    else:
                        self.sock.sendall(bytes("2005","utf8"))

                file_obj=open(local_path,"rb")
                file_obj.seek(has_sent)

                while has_sent<file_size:
                    data=file_obj.read(1024)
                    self.sock.sendall(data)
                    has_sent+=len(data)
                    self.bar(has_sent,file_size)
                file_obj.close()
                print("上传成功")


    def instruction_get(self, instructions):
        if len(instructions) == 1:
            print("Please add the remote filename that you wanna get")
            return
        else:
            file_name = instructions[1]
            command_str = "file_get|%s" % (json.dumps({"file_name": file_name}))
            self.sock.send(command_str.encode())
            server_response = json.loads(self.sock.recv(1024).decode())
            if server_response['response'] == "300":
                file_abs_path = "%s/%s/%s" % (self.USER_HOME, self.login_user, file_name)
                total_file_size = int(server_response['file_size'])
                server_md5 = server_response['md5']

                received_size = 0
                if os.path.exists(file_abs_path):
                    received_size += os.path.getsize(file_abs_path)

                self.sock.send(json.dumps({"response": "301", "received_size": received_size}).encode())

                local_file_obj = open(file_abs_path, "ab")

                while total_file_size != received_size:
                    data = self.sock.recv(4096)
                    received_size += len(data)
                    local_file_obj.write(data)
                    self.show_progress_bar(received_size, total_file_size)
                else:
                    print("file download finishes")
                    local_file_obj.close()
                if server_md5 == hashlib.md5(open(file_abs_path, 'rb').read()).hexdigest():
                    print('file checksum passed')
                else:
                    print('file checksum failed to pass')

            elif server_response['response'] == "302":
                print("File doesn't exist")

    def handle(self):
        self.connect(self.ftp_host, self.ftp_port)
        if self.auth():
            self.interactive()
