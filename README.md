# 牛津3000詞過濾器

這是一個幫助學習者篩選牛津3000詞彙的小工具，可以快速標記已知和未知的單字，並將不認識的單字匯出成PDF檔案。

## 安裝說明

1. 確保您已安裝 Python 3.x 版本
2. 安裝必要套件：

```bash
pip install -r requirements.txt
```

## 使用方法

1. 執行程式：

```bash
python word_filter.py
```

2. 操作介面：
   - 畫面中央會顯示當前單字
   - 使用鍵盤左右方向鍵或按鈕進行操作：
     - 左方向鍵 (←) 或「認識」按鈕：標記為已知單字
     - 右方向鍵 (→) 或「不認識」按鈕：標記為生詞
   - 進度條會顯示目前學習進度
   - 可隨時點擊「匯出生詞PDF」將不認識的單字匯出

![image](/ui.png)

3. 功能特色：
   - 自動保存進度，下次開啟時會從上次離開的地方繼續
   - 可隨時匯出生詞清單為PDF檔案
   - 支援鍵盤快捷鍵，提高操作效率

## 檔案說明

- `word_filter.py`：主程式檔案
- `oxford_3000.txt`：牛津3000詞彙清單
- `progress.json`：進度儲存檔案（自動產生）
- `unknown_words.pdf`：匯出的生詞清單（執行匯出時產生）
- `requirements.txt`：必要套件清單

## 注意事項

1. 請確保 `oxford_3000.txt` 與程式檔案在同一個資料夾中
2. 程式會自動創建 `progress.json` 來儲存進度
3. 匯出的PDF檔案會儲存在程式所在的資料夾中

## 常見問題

Q: 如何重新開始？  
A: 刪除 `progress.json` 檔案即可從頭開始

Q: 如何查看已標記的生詞？  
A: 點擊「匯出生詞PDF」按鈕，即可產生包含所有已標記生詞的PDF檔案

## 系統需求

- Python 3.x
- tkinter（Python內建）
- reportlab（用於生成PDF）