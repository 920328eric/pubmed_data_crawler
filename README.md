
# 自動化爬取Pubmed上完整文獻，輸出pdf和txt檔
# 需先勾選Free full text，並下載 All results (Abstract text 格式)，並把他們放到程式碼 input_data 裡


## 使用說明
1. main_process 是主要執行的地方

2. 在 target_file = "joint_pain.txt" ， 指定想讀取剛剛下載的Abstract text 格式的txt檔

3. 執行之後 control c 暫停，下次可從上次斷掉的地方繼續執行

4. 輸出的檔案會在 output_data 裡

5. side_code 是各部分邏輯，可自行使用

註：程式中斷執行跳出bug，可能是Pubmed完整文獻鎖起來，請再按一次執行，跳過下載那個檔案

## 安裝

自行依據缺少的import，進行install
