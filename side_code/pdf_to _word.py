from pdf2docx import Converter

                
def pdf2word(file_path):

                    file_name = file_path.split('.')[0]

                    doc_file = f'{file_name}.docx'

                    p2w = Converter(file_path)

                    p2w.convert(doc_file, start=0, end=None)

                    p2w.close()

                    return doc_file

if __name__ == '__main__':  
        pdf2word('/Users/chenchongyu/Library/Mobile Documents/com~apple~CloudDocs/Graduation Topic/大三下/TainingMaterials/test/Firebase 圖形畫法.pdf')