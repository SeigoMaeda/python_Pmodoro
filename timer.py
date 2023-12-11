import tkinter as tk

# tk.Frameを継承したApplicationクラスを作成
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        # ウィンドウの設定
        master.title("キッチンタイマー")
        master.geometry("430x200")

        # 実行内容
        self.pack()
        self.create_widget()

    # create_widgetメソッドを定義
    def create_widget(self):

        # 全体の親キャンバス
        self.canvas_bg = tk.Canvas(self.master, width=430, height=200)
        self.canvas_bg.pack()

        # タイマー用のキャンバス
        self.canvas_time = tk.Canvas(self.canvas_bg, width=410, height=80, bg="lightblue")
        self.canvas_time.place(x=10, y=10)

        # startボタン
        self.min_button = tk.Button(self.canvas_bg, width=8, height=2, text="start", font=("MSゴシック体", "18","bold"))
        self.min_button.place(x=10, y=100)

        # stopボタン
        self.sec_button = tk.Button(self.canvas_bg, width=8, height=2, text="stop", font=("MSゴシック体", "18","bold"))
        self.sec_button.place(x=150, y=100)

        # endボタン
        self.reset_button = tk.Button(self.canvas_bg, width=8, height=2, text="end", font=("MSゴシック体", "18","bold"))
        self.reset_button.place(x=290, y=100)


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()