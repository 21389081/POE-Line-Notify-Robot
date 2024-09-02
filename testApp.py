import os
import time
import requests

# 設定
file_path = r"Your log file path here"
line_token = "Your line token here"

def send_line_notify(message):
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
    last_size = os.path.getsize(file_path)
    
    while True:
        current_size = os.path.getsize(file_path)
        if current_size > last_size:
            with open(file_path, "r", encoding="utf-8") as file:
                file.seek(last_size)
                new_content = file.read()
                
            for line in new_content.splitlines():
                if "@來自" in line:  # 這裡請替換為你要檢查的特定字串
                    send_line_notify(line)
                    
            last_size = current_size
        time.sleep(1)

if __name__ == "__main__":
    monitor_file(file_path)
