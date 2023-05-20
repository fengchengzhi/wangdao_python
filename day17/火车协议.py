import struct
import socket


def send_train(s: socket.socket, file_bytes):
    train_head = len(file_bytes)
    train_head_bytes = struct.pack('I', train_head)
    s.send(train_head_bytes + file_bytes)


def recv_train(s: socket.socket):
    train_head = s.recv(4)
    if train_head:
        file_len = struct.unpack('I', train_head)
        data = ''.encode('utf8')
        num = file_len[0]
        while len(data) < file_len[0]:
            data += s.recv(num)
            num -= len(data)
        return data
    else:
        return None
