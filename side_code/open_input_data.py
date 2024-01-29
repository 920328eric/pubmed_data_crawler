import os

current_directory = os.getcwd()

# input_data 的完整路徑
input_data_directory = os.path.join(current_directory, 'input_data')

for root, dirs, files in os.walk(input_data_directory):
    for file in files:
        if file.endswith('.txt'):
            # txt文件的完整路徑
            file_path = os.path.join(root, file)
            # 打開txt文件
            with open(file_path, 'r', encoding='utf-8') as f:
                print(f'文件 {file} 的内容：')
                for i in range(4):
                    line = f.readline()
                    print(line)
                    
                  
