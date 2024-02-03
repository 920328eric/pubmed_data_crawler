import io
import requests
from bs4 import BeautifulSoup
import os
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed


each_file_name = ''
each_file_pmcid = ''
txt_save_path = ''
name = ''
current_line = 0
pdf_save_path = '/Users/chenchongyu/desktop/output_data/pdf'
origin_pdf_path = ''
current_crawler = 1
switch = 'false'

current_directory = os.getcwd()
# input_data 的完整路徑
input_data_directory = os.path.join(current_directory, 'input_data')


# 以檔案紀錄目前爬取到的檔案行數
file_current_crawler_path = 'current_crawler.txt'
# 讀取當前資料號碼
with open(file_current_crawler_path, 'r') as f:
    current_crawler = int(f.read())

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
                return "https://www.ncbi.nlm.nih.gov" + href
                # print("https://www.ncbi.nlm.nih.gov" + href)
                # break
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
    if response.status_code == 200:
        #從伺服器返回的響應內容轉換為 BytesIO 對象，這是一個在記憶體中操作二進制數據的流
        bytes_io = io.BytesIO(response.content)
        with open(save_path + "/%s.PDF" % pdf_name, mode='wb') as f:
            f.write(bytes_io.getvalue())
            print('%s.PDF 下載成功！' % pdf_name)
    else:
        print('無法下載 %s.PDF ！' % pdf_name)


# pdf 轉成 txt 檔
def pdf_to_txt(pdf_path):
        global txt_save_path
        
        # rb以二進位讀取模式開啟本機pdf文件
        fn = open(pdf_path,'rb')
        # 建立一個pdf文檔分析器
        parser = PDFParser(fn)
        # 建立一個PDF文檔
        doc = PDFDocument()
        # 連接分析器 與文檔對象
        parser.set_document(doc)
        doc.set_parser(parser)

	# 提供初始化密碼doc.initialize("lianxipython")
    # 如果沒有密碼 就建立一個空的字串
        doc.initialize("")
    # 偵測文件是否提供txt轉換，不提供就忽略
        if not doc.is_extractable:
             raise PDFTextExtractionNotAllowed
        else:
    	# 建立PDf資源管理器
            resource = PDFResourceManager()
            # 建立一個PDF參數分析器
            laparams = LAParams()
            # 建立聚合器,用於讀取文件的對象
            device = PDFPageAggregator(resource,laparams=laparams)
            #建立解釋器，對文件編碼，解釋成Python能夠辨識的格式
            interpreter = PDFPageInterpreter(resource,device)
            # 循環遍歷列表，每次處理一頁的內容
            # doc.get_pages() 取得page列表
            for page in doc.get_pages():
                # 利用解釋器的process_page()方法解析讀取單獨頁數
                interpreter.process_page(page)
                # 使用聚合器get_result()方法取得內容
                layout = device.get_result()
                # 這裡layout是一個LTPage物件,裡面存放著這個page解析出的各種對象
                for out in layout:
                    # 判斷是否含有get_text()方法，取得我們想要的文字
                    if hasattr(out,"get_text"):
                        #print(out.get_text())
                        with open(txt_save_path,'a') as f:
                            f.write(out.get_text()+'\n')
            print( '第' + str(current_crawler - 1)  + '資料' + '轉換成功！ \n')


# 搜尋檔名、並提取PMCID
def search_file_pmcid(target_file):
    global current_crawler
    global each_file_name
    global each_file_pmcid
    global current_line
    global name
    global txt_save_path
    global origin_pdf_path
    global pdf_save_path
    global switch
    
    for root, dirs, files in os.walk(input_data_directory):
        for file in files:
            # if file.endswith('.txt'):
            if file == target_file :
                # txt文件的完整路徑
                file_path = os.path.join(root, file)
                # 打開txt文件
                with open(file_path, 'r', encoding='utf-8') as f:
                    #for i in range(150):
                    for line in f:
                        if not line:
                            print('資料整理完成!')
                            break
                        if line.startswith(str(current_crawler) + '. '):
                            current_crawler += 1
                            current_line = 1

                            switch = 'true'

                            # 將新數目寫入
                            with open(file_current_crawler_path, 'w') as f:
                                f.write(str(current_crawler))

                        elif (line.startswith('PMCID')) :

                            if (switch == 'true'):
                                
                                switch = 'false'

                                each_file_pmcid = line.split()[-1]
                                if len(name) <= 1:
                                    each_file_name = each_file_pmcid
                                else:
                                    each_file_name = name
                                
                                print('檔名 = ' + each_file_name)
                                print('PMCID = ' + each_file_pmcid  + '\n')

                                origin_pdf_path = f"/Users/chenchongyu/desktop/output_data/pdf/{each_file_name}.pdf"
                                txt_save_path = f"/Users/chenchongyu/desktop/output_data/txt/{each_file_name}.txt"
                                pdf_name = each_file_name

                                pdf_url = find_url("https://www.ncbi.nlm.nih.gov/pmc/articles/" + each_file_pmcid + '/')

                                if pdf_url:
                                    download_pdf(pdf_save_path,pdf_name,pdf_url)
                                    pdf_to_txt(origin_pdf_path)
                                else:
                                    print("找不到 PDF 鏈接，跳過該筆資料。")
                                

                        elif(current_line == 2):
                            name = line
                            current_line +=1
            
                        else:
                            current_line +=1

                            

if __name__ == '__main__':  #主程式，在該文件被直接執行時才會被執行

    target_file = "joint_discomfort.txt" # 指定想讀取的txt檔
    
    try:
        search_file_pmcid(target_file)

    except KeyboardInterrupt:
        current_crawler -= 1
        print('\n')
        print('當前讀到的資料為第', str(current_crawler - 1), '筆')
