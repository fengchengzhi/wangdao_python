nums = [2, 3, 5, 2, 5, 7, 3, 4]  # 8 个数，其中有两个数出现了一次，其他的数都出现了两次

# 对所有的数进行异或操作，得到最终的结果
result = 0
for num in nums:
    result ^= num

# 找到某一位为 1 的位置
bit = 1
while result & bit == 0:
    bit <<= 1

# 根据某一位是否为 1，将所有数分成两个集合
group1, group2 = 0, 0
for num in nums:
    if num & bit == 0:
        group1 ^= num
    else:
        group2 ^= num

# 输出只出现了一次的两个数
print(f"The numbers that appear only once are {group1} and {group2}")
