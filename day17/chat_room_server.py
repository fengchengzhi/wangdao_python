import socket
import select
import sys


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    addr = ('192.168.75.128', 2200)
    s.bind(addr)
    s.listen(128)
    epoll = select.epoll()
    epoll.register(s.fileno(), select.EPOLLIN)
    epoll.register(sys.stdin.fileno(), select.EPOLLIN)
    c_l = []
    c_a_l = []
    while True:
        events = epoll.poll(-1)
        for fd, event in events:
            if fd == s.fileno():
                c, c_addr = s.accept()
                c_l.append(c)
                c_a_l.append(c_addr)
                print(c_addr)
                epoll.register(c.fileno(), select.EPOLLIN)
                continue
            elif fd == sys.stdin.fileno():
                data = input()
                for client0 in c_l:
                    client0.send(data.encode('utf8'))
            else:
                i = 0
                while i < len(c_l):
                    if fd == c_l[i].fileno():
                        data = c_l[i].recv(100)
                        if data:
                            for client0 in c_l:
                                if client0 is not c_l[i]:
                                    client0.send(data)
                        else:
                            print(c_l[i])
                            epoll.unregister(c_l[i].fileno())
                            c_l[i].close()
                            c_l.remove(c_l[i])
                            i -= 1
                    i += 1
    s.close()


if __name__ == '__main__':
    main()
