import os
import time
import requests

# 設定
file_path = r"(Your POE path)\logs\Client.txt"  # 要監控的文件路徑
line_token = "Your LINE Notify Token"  # LINE Notify 的 token

def send_line_notify(message):
    """發送 LINE Notify 通知"""
    url = "https://notify-api.line.me/api/notify"
    headers = {
        "Authorization": "Bearer " + line_token
    }
    data = {
        "message": message,
    }
    response = requests.post(url, headers=headers, data=data)
    return response.status_code

def monitor_file(file_path):
    """監控文件變化並發送通知"""
    last_size = os.path.getsize(file_path)  # 記錄文件的初始大小
    
    while True:
        current_size = os.path.getsize(file_path)  # 獲取當前文件大小
        if current_size > last_size:  # 如果文件大小增加
            with open(file_path, "r", encoding="utf-8") as file:
                file.seek(last_size)  # 將文件指針移動到上次讀取的位置
                new_content = file.read()  # 讀取新增的內容
                
            for line in new_content.splitlines():  # 逐行處理新增的內容
                if "@來自" in line:  # 檢查是否包含特定字串
                    send_line_notify(line)  # 發送 LINE 通知
                    
            last_size = current_size  # 更新文件大小記錄
        time.sleep(1)  # 等待1秒後再次檢查

if __name__ == "__main__":
    monitor_file(file_path)  # 開始監控文件