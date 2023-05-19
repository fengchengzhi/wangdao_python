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
        data = s.recv(file_len[0])
        return data
    else:
        return None
