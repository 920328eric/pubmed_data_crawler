import os

file_current_crawler_path = 'current_crawler.txt'

# 讀取當前數目
with open(file_current_crawler_path, 'r') as f:
    count = int(f.read())

count += 1

# 將新數目寫入
with open(file_current_crawler_path, 'w') as f:
    f.write(str(count))

print('當前累加數目為：', count)
