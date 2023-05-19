import socket
import select
import sys


def main():
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    addr = ('192.168.75.128', 2200)
    c.connect(addr)
    epoll = select.epoll()
    epoll.register(c.fileno(), select.EPOLLIN)
    epoll.register(sys.stdin.fileno(), select.EPOLLIN)
    while True:
        events = epoll.poll(-1)
        for fd, event in events:
            if fd == c.fileno():
                data = c.recv(100).decode('utf8')
                if data:
                    print(data)
                else:
                    print('断开')
                    epoll.unregister(c.fileno())
                    epoll.unregister(sys.stdin.fileno())
                    c.close()
                    return
            elif fd == sys.stdin.fileno():
                data = input()
                c.send(data.encode('utf8'))


if __name__ == '__main__':
    main()
