import io
import requests
from bs4 import BeautifulSoup

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



# if __name__ == '__main__':  #主程式，在該文件被直接執行時才會被執行
#     save_path = '/Users/chenchongyu/Library/Mobile Documents/com~apple~CloudDocs/Graduation Topic/大三下/TainingMaterials'
#     pdf_name = '2007年年度報告'
#     pdf_url = "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7362874/pdf/rapm-2019-101243.pdf"
#     download_pdf(save_path, pdf_name, pdf_url)
        
if __name__ == '__main__':
    find_url("https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7362874/")