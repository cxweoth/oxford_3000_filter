import tkinter as tk
from tkinter import messagebox
import json
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

class WordFilterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("牛津3000詞過濾器")
        
        # 載入資料
        self.load_data()
        
        # GUI元件
        self.word_label = tk.Label(root, text="", font=('Arial', 24))
        self.word_label.pack(pady=20)
        
        # 按鈕框架
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)
        
        self.known_btn = tk.Button(button_frame, text="認識 (←)", command=self.mark_known)
        self.known_btn.pack(side=tk.LEFT, padx=10)
        
        self.unknown_btn = tk.Button(button_frame, text="不認識 (→)", command=self.mark_unknown)
        self.unknown_btn.pack(side=tk.LEFT, padx=10)
        
        self.export_btn = tk.Button(root, text="匯出生詞PDF", command=self.export_pdf)
        self.export_btn.pack(pady=10)
        
        # 顯示進度
        self.progress_label = tk.Label(root, text="")
        self.progress_label.pack(pady=10)
        
        # 添加鍵盤綁定
        self.root.bind('<Left>', lambda event: self.mark_known())
        self.root.bind('<Right>', lambda event: self.mark_unknown())
        
        self.show_next_word()
    
    def load_data(self):
        # 載入牛津3000詞
        with open('oxford_3000.txt', 'r', encoding='utf-8') as f:
            self.words = [line.strip() for line in f.readlines()]
        
        # 載入已儲存的進度
        try:
            with open('progress.json', 'r') as f:
                saved_data = json.load(f)
                self.current_index = saved_data.get('current_index', 0)
                self.unknown_words = set(saved_data.get('unknown_words', []))
        except FileNotFoundError:
            self.current_index = 0
            self.unknown_words = set()
    
    def save_progress(self):
        with open('progress.json', 'w') as f:
            json.dump({
                'current_index': self.current_index,
                'unknown_words': list(self.unknown_words)
            }, f)
    
    def show_next_word(self):
        if self.current_index < len(self.words):
            self.word_label.config(text=self.words[self.current_index])
            self.progress_label.config(
                text=f"進度：{self.current_index + 1}/{len(self.words)}"
            )
        else:
            self.word_label.config(text="完成！")
            self.known_btn.config(state=tk.DISABLED)
            self.unknown_btn.config(state=tk.DISABLED)
    
    def mark_known(self):
        self.current_index += 1
        self.save_progress()
        self.show_next_word()
    
    def mark_unknown(self):
        self.unknown_words.add(self.words[self.current_index])
        self.current_index += 1
        self.save_progress()
        self.show_next_word()
    
    def export_pdf(self):
        try:
            c = canvas.Canvas("unknown_words.pdf", pagesize=letter)
            c.setFont("Helvetica", 12)
            
            # 準備單字列表（加上編號）
            sorted_words = sorted(self.unknown_words)
            numbered_words = [f"{i+1}. {word}" for i, word in enumerate(sorted_words)]
            
            # 設定頁面參數
            words_per_page = 90  # 每頁30行 x 3欄 = 90個單字
            col_x = [50, 220, 390]  # 三欄的x座標
            line_height = 20  # 行高
            
            # 計算頁面垂直居中的起始位置
            page_height = letter[1]  # 獲取頁面高度
            content_height = 30 * line_height  # 30行的總高度
            margin_top = (page_height - content_height) / 2  # 計算上方邊距
            
            # 分頁處理單字
            for page_num, page_start in enumerate(range(0, len(numbered_words), words_per_page)):
                if page_num == 0:  # 只在第一頁顯示標題
                    c.drawString(250, margin_top + content_height + 30, "Unknown Words List")
                    start_y = margin_top + content_height  # 從內容區域的頂部開始
                else:
                    start_y = margin_top + content_height  # 從內容區域的頂部開始
                
                # 取得這一頁要顯示的單字
                page_words = numbered_words[page_start:page_start + words_per_page]
                
                # 在這一頁上繪製單字
                for i, word in enumerate(page_words):
                    # 計算在頁面上的位置
                    col = i % 3  # 決定是第幾欄
                    row = i // 3  # 決定是第幾行
                    x = col_x[col]
                    y = start_y - (row * line_height)
                    
                    c.drawString(x, y, word)
                
                # 如果還有更多單字，就新增一頁
                if page_start + words_per_page < len(numbered_words):
                    c.showPage()
                    c.setFont("Helvetica", 12)
            
            c.save()
            messagebox.showinfo("匯出成功", "生詞已匯出至 unknown_words.pdf")
        except Exception as e:
            messagebox.showerror("錯誤", f"匯出PDF時發生錯誤：\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = WordFilterApp(root)
    root.mainloop() 