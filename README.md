
# 自動化爬取Pubmed上完整文獻，輸出pdf和txt檔
需先到Pubmed搜尋引擎，搜尋想要爬取的文獻關鍵字，並勾選Free full text，最後下載 All results (Abstract text 格式)，把他們放到程式碼 input_data 裡


## 使用說明
1. main_process 是主要執行的地方

2. 在 target_file = "joint_pain.txt" ， 指定想讀取剛剛下載的Abstract text 格式的txt檔

3. 執行之後 control c 暫停，下次可從上次斷掉的地方繼續執行

4. 輸出的檔案會在 output_data 裡

5. side_code 是各部分邏輯，可自行使用

註：有些檔案無法下載，可能是Pubmed完整文獻鎖起來，程式會自行跳過下載那個檔案

（同時等待100-600的隨機秒數，以防你的IP被鎖起來）


註：有些檔名會以PMCID代替，為了爬取資料的方便

警告：使用此程式你的網路 IP 可能被鎖

## 安裝

自行依據缺少的import，進行install
