def count_binary_ones(num):
    # 将输入的整数转换为其对应的二进制字符串
    binary_str = bin(num & 0xffffffffffffffff)[2:]  # 将负数按64位处理

    # 遍历二进制字符串，统计其中为 "1" 的字符的个数
    count = 0
    for c in binary_str:
        if c == "1":
            count += 1

    # 输出统计结果
    print(f"Number of ones in binary representation of {num}: {count}")


# 测试示例
count_binary_ones(int(input()))
