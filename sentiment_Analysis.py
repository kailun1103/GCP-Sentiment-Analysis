import csv
from google.cloud import language_v2
import os
import time
from multiprocessing import Pool, cpu_count

# 設定認證憑證文件路徑
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'Cloud Natural Language Key.json'

# 定義情感分析的函式
def emotion_analysis(text):
    try:
        # 實例化客戶端
        client = language_v2.LanguageServiceClient()

        # 執行情感分析
        document = language_v2.Document(
            content=text,
            type_=language_v2.Document.Type.PLAIN_TEXT)
        sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment

        return sentiment.score  # 回傳情感分析的分數
    except Exception as e:
        # print(f"情感分析錯誤: {e}")
        return 0  # 若發生錯誤，回傳結果為0

# 指定您的CSV檔案路徑
csv_file_path = 'test.csv'
# 暫存檔案路徑
temp_file_path = 'temp.csv'

# 處理每一列資料的函式
def process_row(row):
    if len(row) >= 3:
        data = row[2]  # 第三欄的資料
        sentiment_score = emotion_analysis(data)  # 進行情感分析，獲得情感分數
        row.append(sentiment_score)  # 將情感分數加入該列的最後一欄
    else:
        row.append(None)  # 如果第三欄不存在資料，將情感分數設定為 None
    return row

if __name__ == '__main__':
    start_time = time.time()  # 開始時間
    processed_count = 0  # 處理行數計數

    with open(csv_file_path, 'r', encoding='utf-8-sig') as file, open(temp_file_path, 'w', newline='', encoding='utf-8-sig') as temp_file:
        csv_reader = csv.reader(file)
        csv_writer = csv.writer(temp_file)

        # 建立多進程池，設定進程數和每個子進程執行的任務數
        pool = Pool(processes=8, maxtasksperchild=4)

        # 以平行方式處理每一列資料
        for processed_row in pool.imap(process_row, csv_reader):
            csv_writer.writerow(processed_row)  # 將處理過的資料寫入暫時檔案
            processed_count += 1
            print(f'目前處理進度: [ {processed_count} ] - 經過時間: {time.time() - start_time:.2f} 秒')

        pool.close()
        pool.join()

    # 將暫時檔案的內容複製回原始檔案
    import shutil
    shutil.move(temp_file_path, csv_file_path)
