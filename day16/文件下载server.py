import socket
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
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    adrr = ('192.168.1.121', 2200)
    s.bind(adrr)
    s.listen(128)
    c, c_addr = s.accept()
    file_name = recv_train(c)
    f = open(file_name, 'rb')
    st = f.readline()
    st = st.replace(b'\r\n', b'\n')
    while st:
        send_train(c, st)
        st = f.readline()
        st = st.replace(b'\r\n', b'\n')
    f.close()
    c.close()
    s.close()


if __name__ == '__main__':
    download_file()
