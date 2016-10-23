import os, sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from conf import settings
import socketserver
from modules import threading_socket_server

class ArgvHandler:

    def __init__(self, args):
        self.args = args
        self.argv_parse()

    def argv_parse(self):
        if len(self.args) < 1:
            self.help_msg()
        else:
            first_argv = self.args[1]
            if hasattr(self, first_argv):
                func = getattr(self, first_argv)
                func()
            else:
                self.help_msg()

    def help_msg(self):
        msg = '''
            start
            stop
        '''
        print(msg)

    def start(self):
        try:
            print("starting...")
            server = socketserver.ThreadingTCPServer((settings.BIND_HOST, settings.BIND_PORT), threading_socket_server.MyTCPHandler)
            print('server started')
            server.serve_forever()
        except KeyboardInterrupt:
            pass
