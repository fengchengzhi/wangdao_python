file1 = open('file.txt', 'r+', encoding='utf8')
while 1:
    text = file1.readline()
    print(text, end='')
    if not text:
        break
file1.close()
