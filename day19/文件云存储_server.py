import socket
import os
import struct
from multiprocessing.pool import Pool


class Server:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.listen: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def s_init(self):
        self.listen.bind((self.ip, self.port))
        self.listen.listen(128)

    def start(self):
        po = Pool(3)
        while True:
            client, client_addr = self.listen.accept()
            if client:
                print(client_addr)
                user = User(client, client_addr)
                po.apply_async(self._deal_command, args=(user,))

    def _deal_command(self, user):
        user.deal_command()


class User:
    def __init__(self, c, addr):
        self.name = None
        self.c: socket.socket = c
        self.path = os.getcwd()
        self.addr = addr
        self._flag = 0

    def _gets_file(self, file_name):
        self._send_train(file_name.encode('utf8'))
        f = open(file_name, 'rb')
        st = f.readline()
        st = st.replace(b'\r\n', b'\n')
        while st:
            self._send_train(st)
            st = f.readline()
            st = st.replace(b'\r\n', b'\n')
        self._send_train('成功'.encode('utf8'))
        f.close()

    def _puts_file(self):
        file_name = self._recv_train().decode('utf8')
        f = open(file_name, 'wb')
        while True:
            a = self._recv_train()
            if a == '成功'.encode('utf8'):
                break
            f.write(a)
        f.close()

    def deal_command(self):
        while True:
            com = self._recv_train().decode('utf8')
            if com[:2] == 'ls':
                self._deal_ls()
            elif com[:3] == 'pwd':
                self._deal_pwd()
            elif com[:2] == 'rm':
                self._deal_rm(com)
            elif com[:4] == 'puts':
                self._deal_puts(com)
            elif com[:4] == 'gets':
                self._deal_gets(com, self._flag)
            elif com[:2] == 'cd':
                self._deal_cd(com)
            elif com[:4] == 'exit':
                break
            elif com is None:
                break
        self.c.close()

    def _deal_ls(self):
        data = ''
        for i in os.listdir(self.path):
            if os.path.isdir(i):
                data += i + '\t' * 3 + str(os.stat(i).st_size) + '\t' + 'dir' + '\n'
            else:
                data += i + '\t' * 3 + str(os.stat(i).st_size) + '\t' + 'file' + '\n'
        if data is None:
            data = '\n'
        else:
            data = data[:-1]
        self._send_train(data.encode('utf8'))

    def _deal_cd(self, com):
        com = com.split()[1]
        if os.path.isdir(self.path + '/' + com):
            os.chdir(self.path + '/' + com)
            self._send_train(('当前工作目录' + os.getcwd()).encode('utf8'))
            self.path = os.getcwd()
        else:
            self._send_train('请输入文件夹'.encode('utf8'))

    def _deal_gets(self, com, flag):
        com = com.split()[-1]
        if os.path.isfile(com):
            self._send_train('0'.encode('utf8'))
            self._gets_file(com)
        else:
            self._send_train('1'.encode('utf8'))
            file_list = os.listdir(com)
            self._send_train(com.encode('utf8'))
            for file in file_list:
                self._deal_gets(com + '/' + file, flag + 1)
        if flag == 0:
            self._send_train('2'.encode('utf8'))

    def _deal_puts(self, com):
        while True:
            data = self._recv_train().decode('utf8')
            if data == '0':
                self._puts_file()
            elif data == '1':
                dir_name = self._recv_train().decode('utf8')
                os.mkdir(dir_name)
                com = com + '/' + dir_name
            elif data == '2':
                return

    def _deal_pwd(self):
        self._send_train(os.getcwd().encode('utf8'))

    def _deal_rm(self, com):
        com = com.split()[-1]
        if os.path.isfile(com):
            os.remove(com)
        else:
            file_list = os.listdir(com)
            for file in file_list:
                self._deal_rm(com + '/' + file)
            os.rmdir(com)

    def _send_train(self, file_bytes):
        train_head = len(file_bytes)
        train_head_bytes = struct.pack('I', train_head)
        self.c.send(train_head_bytes + file_bytes)

    def _recv_train(self):
        train_head = self.c.recv(4)
        if train_head:
            file_len = struct.unpack('I', train_head)
            data = self.c.recv(file_len[0])
            return data
        else:
            return None


if __name__ == '__main__':
    s = Server('192.168.75.128', 2200)
    s.s_init()
    s.start()
