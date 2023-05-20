import socket
import sys
import struct


def send_train(s: socket.socket, file_bytes):
    train_head = len(file_bytes)
    train_head_bytes = struct.pack('I', train_head)
    s.send(train_head_bytes + file_bytes)


def recv_train(s: socket.socket):
    train_head = s.recv(4)
    if train_head:
        file_len = struct.unpack('I', train_head)
        data = s.recv(file_len[0])
        return data
    else:
        return None


def download_file():
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    adrr = ('192.168.1.121', 2200)
    c.connect(adrr)
    send_train(c, b'python.txt')
    name = sys.argv[1]
    f = open(name, 'wb')
    while True:
        a = recv_train(c)
        if not a:
            break
        f.write(a)
    f.close()
    c.close()


if __name__ == '__main__':
    download_file()
