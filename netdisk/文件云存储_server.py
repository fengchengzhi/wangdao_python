import socket, concurrent.futures, os, struct, select, sys, random, string, concurrent.futures, pymysql


class Mysql:
    def __init__(self):
        self.con = pymysql.connect(host='192.168.75.128', port=3306, database='netdisk',
                                   user='root', password='123456')

    def compare_password(self, name, password):
        # 判断密码是否正确,返回是否正确以及token
        cs1 = self.con.cursor()
        result = cs1.execute('select user_password,token from users where %s=user_name', name)
        if result != 1:
            cs1.close()
            raise Exception('wrong')
        else:
            a, b = cs1.fetchall()[0]
            if password == a:
                cs1.close()
                return True, b
            else:
                cs1.close()
                return False, None

    def insert_name(self, name, password, token):
        # 插入新用户
        cs1 = self.con.cursor()
        result = cs1.execute('insert into users values(0,%s,%s,%s)', (name, password, token))
        if result != 1:
            raise Exception('wrong')
        self.con.commit()
        cs1.close()


class Server:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        # 服务器端对象
        self.listen: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.epoll = select.epoll()
        self.path = os.getcwd()

    def s_init(self):
        self.listen.bind((self.ip, self.port))
        self.listen.listen(128)
        # 注册epoll
        self.epoll.register(self.listen.fileno(), select.EPOLLIN)
        self.epoll.register(sys.stdin.fileno(), select.EPOLLIN)

    def deal_command(self, user):
        user.deal_command()

    def start(self):
        # 创建线程池
        executor = concurrent.futures.ThreadPoolExecutor()
        # po=Pool(3)
        # 保存套接字对象和token
        user_list = []
        sql = Mysql()
        while True:
            events = self.epoll.poll(-1)
            for fd, event in events:
                # 退出
                if fd == sys.stdin.fileno():
                    if input() == 'exit':
                        sql.con.close()
                        return
                # 有新客户端链接
                elif fd == s.listen.fileno():
                    new_client, client_addr = self.listen.accept()
                    print(client_addr)
                    user = User(new_client, client_addr)
                    # 首先判断是什么连接，token或者用户名或者密码
                    temp = user.recv_train().decode('utf8')
                    # 注册
                    if temp == '0':
                        name = user.recv_train().decode('utf8')
                        password = user.recv_train().decode('utf8')
                        letters = string.ascii_letters + string.digits
                        user_token = ''.join(random.choice(letters) for _ in range(20))
                        sql.insert_name(name, password, user_token)
                        # 发送token
                        user.send_train('注册成功'.encode('utf8'))
                        user.send_train(user_token.encode('utf8'))
                        user_list.append(user)
                        self.epoll.register(user.c.fileno(), select.EPOLLIN)
                        user.name = name
                        os.mkdir(self.path + '/' + user.name)
                        user.path = self.path + '/' + user.name
                    # 登录
                    elif temp == '1':
                        name = user.recv_train().decode('utf8')
                        while True:
                            password = user.recv_train().decode('utf8')
                            r_bool, token = sql.compare_password(name, password)
                            if r_bool:
                                user.send_train('登录成功'.encode('utf8'))
                                user.send_train(token.encode('utf8'))
                                self.epoll.register(user.c.fileno(), select.EPOLLIN)
                                break
                            else:
                                user.send_train('密码错误,请重新输入'.encode('utf8'))
                        user_list.append(user)
                        user.name = name
                        user.path = self.path + '/' + user.name
                    # 下载
                    elif temp == '2':
                        executor.submit(self.deal_command, user)
                else:
                    # 执行简单命令
                    for key in list(user_list):
                        if fd == key.c.fileno():
                            if key.deal_command() is None:
                                print(f'{key.name}退出')
                                self.epoll.unregister(key.c.fileno())
                                key.c.close()
                                user_list.remove(key)


class User:
    def __init__(self, c, addr):
        self.name = None
        self.c: socket.socket = c
        self.path = None
        self.addr = addr
        self._flag = 0

    def _gets_file(self, file_name):
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

    def _puts_file(self):
        file_name = self.recv_train().decode('utf8')
        f = open(file_name, 'wb')
        while True:
            a = self.recv_train()
            if a == ''.encode('utf8'):
                break
            f.write(a)
        f.close()

    def deal_command(self):
        try:
            com = self.recv_train().decode('utf8')
        except AttributeError as e:
            return
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
            return
        return 1

    def _deal_ls(self):
        data = ''
        for i in os.listdir(self.path):
            if os.path.isdir(self.path + '/' + i):
                data += i + '\t' * 3 + str(os.stat(self.path + '/' + i).st_size) + '\t' + 'dir' + '\n'
            else:
                data += i + '\t' * 3 + str(os.stat(self.path + '/' + i).st_size) + '\t' + 'file' + '\n'
        if data is None:
            data = '\n'
        else:
            data = data[:-1]
        self.send_train(data.encode('utf8'))

    def _deal_cd(self, com):
        com = com.split()[1]
        if os.path.isdir(self.path + '/' + com):
            os.chdir(self.path + '/' + com)
            self.send_train(('当前工作目录' + os.getcwd().replace(PATH + '/' + self.name, '')).encode('utf8'))
            self.path = os.getcwd()
        else:
            self.send_train('请输入文件夹'.encode('utf8'))

    def _deal_gets(self, com, flag):
        com = com.split()[-1]
        if os.path.isfile(com):
            self.send_train('0'.encode('utf8'))
            self._gets_file(com)
        else:
            self.send_train('1'.encode('utf8'))
            file_list = os.listdir(com)
            self.send_train(com.encode('utf8'))
            for file in file_list:
                self._deal_gets(com + '/' + file, flag + 1)
        if flag == 0:
            self.send_train('2'.encode('utf8'))

    def _deal_puts(self, com):
        while True:
            data = self.recv_train().decode('utf8')
            if data == '0':
                self._puts_file()
            elif data == '1':
                dir_name = self.recv_train().decode('utf8')
                os.mkdir(dir_name)
                com = com + '/' + dir_name
            elif data == '2':
                return

    def _deal_pwd(self):
        self.send_train(os.getcwd().replace(PATH + '/' + self.name, '/').encode('utf8'))

    def _deal_rm(self, com):
        com = com.split()[-1]
        if os.path.isfile(com):
            os.remove(com)
        else:
            file_list = os.listdir(com)
            for file in file_list:
                self._deal_rm(com + '/' + file)
            os.rmdir(com)

    def send_train(self, file_bytes):
        train_head = len(file_bytes)
        train_head_bytes = struct.pack('I', train_head)
        self.c.send(train_head_bytes + file_bytes)

    def recv_train(self):
        train_head = self.c.recv(4)
        if train_head:
            file_len = struct.unpack('I', train_head)
            data = ''.encode('utf8')
            num = file_len[0]
            while len(data) < file_len[0]:
                data += self.c.recv(num)
                num = file_len[0]
                num -= len(data)
            return data
        else:
            return None


if __name__ == '__main__':
    s = Server('192.168.75.128', 2200)
    s.s_init()
    PATH = s.path
    s.start()
    s.listen.close()
