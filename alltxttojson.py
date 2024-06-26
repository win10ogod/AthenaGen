import os
import random
import multiprocessing
from tqdm import tqdm
import json

data = "./cleaned3/"

def process_files(file_list):
     all_text = []
     for filename in file_list:
         with open(data + filename, encoding='utf-8') as f:
             lines = f.read()
             lines = lines.split('\n') # 以換行符號分割文本
             text = '\n'.join(f"{i + 1}:{line}" for i, line in enumerate(lines) if line.strip()) # 新增行號
         all_text.append({"text": text})
     return all_text

if __name__ == '__main__':
     lst = os.listdir(data)
     random.shuffle(lst)
     num = len(lst)
     cnt = 1
     batch_size = 10 # 定義每個 JSON 檔案包含的文字檔案數量

     # 使用多進程處理文件
     pool = multiprocessing.Pool(processes=multiprocessing.cpu_count()) # 使用 CPU 核心數量的進程

     # 使用 tqdm 顯示進度條
     with tqdm(total=num, desc="Processing Files") as pbar:
         while cnt < num:
             batch_files = lst[cnt:cnt + batch_size] # 取得下一個批次的檔案列表
             batch_text = pool.map(process_files, [batch_files])[0]
             cnt += batch_size
             pbar.update(batch_size) # 更新進度條

             # 將批次的文字轉換為 JSON 陣列
             output_json = [{"text": entry["text"]} for entry in batch_text]

             # 將 JSON 寫入文件
             json_filename = f'data{cnt // batch_size:02d}.json' # 根據 cnt 計算輸出檔案的名稱
             with open(json_filename, 'w', encoding='utf-8') as json_file:
                 json.dump(output_json, json_file, ensure_ascii=False, indent=4) # 寫入整個列表

     pool.close()
     pool.join()

     print("JSON files have been created.")
