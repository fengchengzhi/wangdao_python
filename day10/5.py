file1 = open('file.txt', 'r', encoding='utf8')
file2 = open('copy.txt', 'a+', encoding='utf8')
while 1:
    text = file1.readline()
    file2.write(text)
    if not text:
        break
file1.close()
file2.close()
