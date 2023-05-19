import os
import socket
import struct


class Client:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name = None
        self._flag = 0

    def c_init(self):
        self.connect.connect((self.ip, self.port))

    def _puts_file(self, file_name):
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

    def _gets_file(self):
        file_name = self._recv_train().decode('utf8')
        f = open(file_name, 'wb')
        while True:
            a = self._recv_train()
            if a == '成功'.encode('utf8'):
                break
            f.write(a)
        f.close()

    def send_command(self):
        while True:
            com = input()
            self._send_train(com.encode('utf8'))
            if com[:2] == 'ls':
                self._send_ls()
            elif com[:3] == 'pwd':
                self._send_pwd()
            elif com[:2] == 'rm':
                self._send_rm()
            elif com[:4] == 'puts':
                self._send_puts(com, self._flag)
            elif com[:4] == 'gets':
                self._send_gets(com)
            elif com[:2] == 'cd':
                self._send_cd()
            elif com[:4] == 'exit':
                break
            else:
                print('输入错误，请重新输入')
        self.connect.close()

    def _send_ls(self):
        data = self._recv_train()
        print(data.decode('utf8'))

    def _send_cd(self):
        data = self._recv_train()
        print(data.decode('utf8'))

    def _send_gets(self, com):
        while True:
            data = self._recv_train().decode('utf8')
            if data == '0':
                self._gets_file()
            elif data == '1':
                dir_name = self._recv_train().decode('utf8')
                os.mkdir(dir_name)
                com = com + '/' + dir_name
            elif data == '2':
                break
        print('成功')

    def _send_puts(self, com, flag):
        com = com.split()[-1]
        if os.path.isfile(com):
            self._send_train('0'.encode('utf8'))
            self._puts_file(com)
        else:
            self._send_train('1'.encode('utf8'))
            file_list = os.listdir(com)
            self._send_train(com.encode('utf8'))
            for file in file_list:
                self._send_puts(com + '/' + file, flag + 1)
        if flag == 0:
            self._send_train('2'.encode('utf8'))
            print('成功')

    def _send_pwd(self):
        data = self._recv_train()
        print(data.decode('utf8'))

    def _send_rm(self):
        pass

    def _send_train(self, file_bytes):
        train_head = len(file_bytes)
        train_head_bytes = struct.pack('I', train_head)
        self.connect.send(train_head_bytes + file_bytes)

    def _recv_train(self):
        train_head = self.connect.recv(4)
        if train_head:
            file_len = struct.unpack('I', train_head)
            data = self.connect.recv(file_len[0])
            return data
        else:
            return None


if __name__ == '__main__':
    c = Client('192.168.75.128', 2200)
    c.c_init()
    c.send_command()
