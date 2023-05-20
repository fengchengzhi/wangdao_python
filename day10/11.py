import os


def dfs(path, width):
    file_list = os.listdir(path)
    for filename in file_list:  # 遍历当前目录下的所有文件
        print(' ' * width + filename)
        if os.path.isdir(path + '/' + filename):  # 如果是目录
            dfs(path + '/' + filename, width + 4)


dfs('../', 0)
