import io
import requests
from bs4 import BeautifulSoup
import os

current_directory = os.getcwd()
# input_data 的完整路徑
input_data_directory = os.path.join(current_directory, 'input_data')


# 以檔案紀錄目前爬取到的檔案行數
file_current_crawler_path = 'current_crawler.txt'
# 讀取當前行數
with open(file_current_crawler_path, 'r') as f:
    current_crawler = int(f.read())


def search_file_pmcid(target_file):
    global current_crawler

    for root, dirs, files in os.walk(input_data_directory):
        for file in files:
            # if file.endswith('.txt'):
            if file == target_file :
                # txt文件的完整路徑
                file_path = os.path.join(root, file)
                # 打開txt文件
                with open(file_path, 'r', encoding='utf-8') as f:
                    #print(f'文件 {file} 的内容：')
                    for i in range(60):
                        current_crawler +=1
                        line = f.readline()
                        if(line.startswith('PMCID')):
                            print(line, end='')
                        #print(line, end='')
                    
                    # 將新數目寫入
                    with open(file_current_crawler_path, 'w') as f:
                        f.write(str(current_crawler))


# pmcid 的網址
def find_url(PMC_url):
    send_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
    "Connection": "keep-alive",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"
    }

    response = requests.get(PMC_url, headers=send_headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a')

        for link in links:

            href = link.get('href')
        
            if href.startswith('/pmc/articles/') and href.endswith('.pdf'):
                print("https://www.ncbi.nlm.nih.gov" + href)
                break
    else:
        print("請求失敗，狀態碼：", response.status_code)


# pmcid網址 對應的 pdf 下載
def download_pdf(save_path, pdf_name, pdf_url):
    send_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        "Connection": "keep-alive",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"
    }
    response = requests.get(pdf_url, headers=send_headers)
    #從伺服器返回的響應內容轉換為 BytesIO 對象，這是一個在記憶體中操作二進制數據的流
    bytes_io = io.BytesIO(response.content)
    with open(save_path + "/%s.PDF" % pdf_name, mode='wb') as f:
        f.write(bytes_io.getvalue())
        print('%s.PDF 下載成功！' % pdf_name)


if __name__ == '__main__':  #主程式，在該文件被直接執行時才會被執行

    target_file = "joint_pain.txt" # 指定想讀取的txt檔
    save_path = '/Users/chenchongyu/Library/Mobile Documents/com~apple~CloudDocs/Graduation Topic/大三下/TainingMaterials/output_data'
    pdf_name = '2007年年度報告'
    pdf_url = find_url("https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7362874/")

    search_file_pmcid(target_file)
    print('\n')
    print('當前讀到的行數為：', current_crawler)
    #download_pdf(save_path, pdf_name, pdf_url)
