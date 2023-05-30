import os
import socket
import struct
import threading


class Client:
    def __init__(self, ip, port, name, password):
        self.ip = ip
        self.port = port
        self.connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name = name
        self.token = None
        self._flag = 0
        self.password = password

    def c_init(self, flag):
        self.connect.connect((self.ip, self.port))
        self.send_train(flag.encode('utf8'))
        if flag == '0':
            # 注册
            self.send_train(self.name.encode('utf8'))
            self.send_train(self.password.encode('utf8'))
            temp = self.recv_train().decode('utf8')
            self.token = self.recv_train().decode('utf8')
            print(temp)
        elif flag == '1':
            # 登录
            self.send_train(self.name.encode('utf8'))
            while True:
                self.send_train(self.password.encode('utf8'))
                temp = self.recv_train().decode('utf8')
                if temp != '登录成功':
                    print(temp)
                    self.password = input()
                else:
                    self.token = self.recv_train().decode('utf8')
                    break
            print(temp)
        elif flag == '2':
            # 下载或上传
            pass

    def _puts_file(self, file_name):
        self.send_train(file_name.encode('utf8'))
        f = open(file_name, 'rb')
        while True:
            data = f.read(10000)
            if data:
                self.send_train(data)
            else:
                self.send_train(''.encode('utf8'))
                break
        f.close()

    def _gets_file(self):
        file_name = self.recv_train().decode('utf8')
        f = open(file_name, 'ab')
        while True:
            a = self.recv_train()
            if a == ''.encode('utf8'):
                break
            f.write(a)
        f.close()

    def send_command(self):
        while True:
            com = input()
            if com[:2] == 'ls' or com[:3] == 'pwd' or com[:2] == 'rm' or com[:2] == 'cd':
                self.send_train(com.encode('utf8'))
            if com[:2] == 'ls':
                self._send_ls()
            elif com[:3] == 'pwd':
                self._send_pwd()
            elif com[:2] == 'rm':
                self._send_rm()
            elif com[:4] == 'puts':
                t1 = threading.Thread(target=puts, args=(self.ip, self.port, com, self.token, self.name, self.password))
                t1.start()
            elif com[:4] == 'gets':
                t2 = threading.Thread(target=gets, args=(self.ip, self.port, com, self.token, self.name, self.password))
                t2.start()
            elif com[:2] == 'cd':
                self._send_cd()
            elif com[:4] == 'exit':
                break
            else:
                print('输入错误，请重新输入')
        self.connect.close()

    def _send_ls(self):
        data = self.recv_train()
        print(data.decode('utf8'))

    def _send_cd(self):
        data = self.recv_train()
        print(data.decode('utf8'))

    def send_gets(self, com):
        while True:
            data = self.recv_train().decode('utf8')
            if data == '0':
                self._gets_file()
            elif data == '1':
                dir_name = self.recv_train().decode('utf8')
                os.mkdir(dir_name)
                com = com + '/' + dir_name
            elif data == '2':
                break
        print('成功')

    def send_puts(self, com, flag):
        com = com.split()[-1]
        if os.path.isfile(com):
            self.send_train('0'.encode('utf8'))
            self._puts_file(com)
        else:
            self.send_train('1'.encode('utf8'))
            file_list = os.listdir(com)
            self.send_train(com.encode('utf8'))
            for file in file_list:
                self.send_puts(com + '/' + file, flag + 1)
        if flag == 0:
            self.send_train('2'.encode('utf8'))
            print('成功')

    def _send_pwd(self):
        data = self.recv_train()
        print(data.decode('utf8'))

    def _send_rm(self):
        pass

    def send_train(self, file_bytes):
        train_head = len(file_bytes)
        train_head_bytes = struct.pack('I', train_head)
        self.connect.send(train_head_bytes + file_bytes)

    def recv_train(self):
        train_head = self.connect.recv(4)
        if train_head:
            file_len = struct.unpack('I', train_head)
            data = ''.encode('utf8')
            num = file_len[0]
            while len(data) < file_len[0]:
                data += self.connect.recv(num)
                num -= len(data)
            return data
        else:
            return None


def gets(ip, port, com, token, name, password):
    client = Client(ip, port, name, password)
    client.name = name
    client.token = token
    client.c_init('2')
    client.send_train(com.encode('utf8'))
    client.send_gets(com)
    client.connect.close()


def puts(ip, port, com, token, name, password):
    client = Client(ip, port, name, password)
    client.name = name
    client.token = token
    client.c_init('2')
    client.send_train(com.encode('utf8'))
    client.send_puts(com, 0)
    client.connect.close()


def main():
    print("请选择注册或者登录：\n0：注册\n1：登录")
    temp = input()
    print('请输入用户名：')
    name = input()
    print('请输入密码：')
    password = input()
    c = Client('192.168.75.128', 2200, name, password)
    c.c_init(temp)
    c.send_command()


if __name__ == '__main__':
    main()
