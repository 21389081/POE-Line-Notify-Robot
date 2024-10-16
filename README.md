# Poe Line Notify App

此程式能在遊戲內收到訊息時，通過 LINE Notify 發送即時通知。


## 功能介紹

這段 Python 程式碼的主要功能是：
1. **文件監控**：不斷監控指定的日誌文件 (`Client.txt`) 是否發生變化。
2. **條件過濾**：當檢測到文件中新增的內容包含特定字串（如 `@來自`）時，進行處理。
3. **LINE 通知**：如果發現符合條件的內容，程式將自動通過 LINE Notify 來發送通知。

這樣的功能非常適合應用於監控日誌文件變化，並及時獲取通知，以便做出快速反應。

## 原理

1. **文件監控機制**

   程式利用 `os.path.getsize()` 來取得文件的大小，以此判斷文件是否有新增內容。每隔 1 秒鐘檢查一次文件大小的變化，如果發現文件大小增加，則表示文件有新增內容。

   ```python
   last_size = os.path.getsize(file_path)  # 記錄文件的初始大小
   while True:
       current_size = os.path.getsize(file_path)  # 獲取當前文件大小
       if current_size > last_size:
           # 讀取新增的內容
           ...
       time.sleep(1)
   ```

2. **讀取新增內容**

   當檢測到文件變大時，利用 `file.seek(last_size)` 將文件指針移動到上次讀取的位置，只讀取新增的內容，從而避免重複讀取之前的內容。

   ```python
   with open(file_path, "r", encoding="utf-8") as file:
       file.seek(last_size)  # 將文件指針移動到上次讀取的位置
       new_content = file.read()  # 讀取新增的內容
   ```

3. **條件過濾與發送通知**

   程式會將新增的內容逐行分割，然後判斷每行是否包含特定的字串（`@來自`）。如果條件符合，就調用 `send_line_notify()` 函數來發送通知。

   ```python
   for line in new_content.splitlines():
       if "@來自" in line:
           send_line_notify(line)  # 發送 LINE 通知
   ```

4. **LINE Notify API 通知推送**

   利用 `requests` 庫來向 LINE Notify API 發送 POST 請求，將符合條件的內容作為通知消息發送給使用者。

   ```python
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
   ```

## 如何使用

### 1. 環境準備

首先，確保已經安裝了 Python 並且安裝了所需的第三方庫 `requests`。可以使用以下指令來安裝：

```sh
pip install requests
```

### 2. 設定 LINE Notify Token

- 前往 [LINE Notify 官方網站](https://notify-bot.line.me/zh_TW/) 並申請一個通知 Token。
- 將程式中的 `line_token` 替換為你獲取的 Token。

### 3. 修改文件路徑

將 `file_path` 修改為你想要監控的日誌文件的路徑。請注意需要使用完整路徑，例如：

```python
file_path = r"C:\Program Files\Path of Exile\logs\Client.txt"
```

### 4. 運行程式

完成以上設置後，可以運行 Python 程式：

```sh
python script_name.py
```

程式會自動開始監控文件變化，當發現新內容並且符合條件時，會自動發送 LINE 通知給你。

## 注意事項

1. **權限問題**：監控文件時需要保證程式有權限讀取該文件，否則會引發錯誤。
2. **Token 安全性**：LINE Notify 的 Token 是敏感信息，請不要將它公開或者提交到公共代碼庫中。
3. **性能考量**：程式每秒檢查一次文件變化，對於頻繁更新的文件來說可能會占用一定的 CPU 資源。可以根據需要調整 `time.sleep()` 的等待時間來平衡性能與即時性。

## 補充

此程式並非本人原創，乃借鑑、參考了網路上的各類資源製作而成，而Line Notify也將在2025年4月1日中止服務，屆時此程式將無法正常運作。

