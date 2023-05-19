import socket

c = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
addr = ('192.168.75.128', 2200)
c.sendto('你好'.encode('utf8'), addr)
temp = c.recvfrom(100)
print(temp)
c.close()