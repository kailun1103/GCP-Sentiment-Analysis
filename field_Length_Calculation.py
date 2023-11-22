import csv

# 指定您的CSV檔案路徑
csv_file_path = 'output_comment_data_1120.csv'

# 打開CSV檔案，同時建立寫入的暫時檔案
with open(csv_file_path, 'r', encoding='utf-8-sig') as file, open('temp.csv', 'w', newline='', encoding='utf-8-sig') as temp_file:
    csv_reader = csv.reader(file)
    csv_writer = csv.writer(temp_file)

    for row in csv_reader:
        
        if len(row) >= 3:
            data = row[2]  # 第三欄的資料
            length = len(data)  # 計算資料的長度
            row.append(length)  # 將長度資料加入該列的最後一欄
        else:
            row.append(None)  # 如果第三欄不存在資料，將長度設定為 None
        
        csv_writer.writerow(row)  # 將處理過的資料寫入暫時檔案中

# 將暫時檔案的內容複製回原始檔案
import shutil
shutil.move('temp.csv', csv_file_path)
