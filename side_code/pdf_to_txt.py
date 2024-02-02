from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed

def parse(pdf_path):
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
                        with open('test.txt','a') as f:
                            f.write(out.get_text()+'\n')
            print('轉換成功！')

if __name__ == '__main__':
	parse('Firebase 圖形畫法.pdf')