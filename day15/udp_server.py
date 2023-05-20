import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
addr = ('192.168.1.121', 2200)
s.bind(addr)
_, ad2 = s.recvfrom(100)
print(_.decode('utf8'))
s.sendto(b'hello', ad2)
s.close()
