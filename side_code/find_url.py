import requests
from bs4 import BeautifulSoup

send_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
    "Connection": "keep-alive",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"
}

url = 'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7362874/'  

response = requests.get(url, headers=send_headers)

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


#https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8855924/pdf/fimmu-13-811402.pdf