# 標準ライブラリ
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk

# サードパーティライブラリ
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ローカル
from app.db_manager import DatabaseManager
from app.timer import Timer


class Application(tk.Frame):
    TITLE_NAME_MAIN_MENU = "Main Menu"
    TITLE_NAME_TIMER = "Pomodoro Timer"
    TITLE_NAME_INPUT = "Input Data"
    TITLE_NAME_LEARNING_DATA = "Learning Data"
    
    WINDOW_SIZE_MAIN_MENU = "480x80"
    WINDOW_SIZE_TIMER = "430x200"
    WINDOW_SIZE_INPUT = "600x100"
    WINDOW_SIZE_LEARNING_DATA = "1030x600"
    
    DB_FILE = "learning_data"

    def __init__(self, master=None):
        super().__init__(master)
        self.db_manager = DatabaseManager(self.DB_FILE)
        master.title(self.TITLE_NAME_MAIN_MENU)
        master.geometry(self.WINDOW_SIZE_MAIN_MENU)
        
        self.current_week_start = datetime.now() - timedelta(days=datetime.now().weekday())
        self.selected_period = tk.StringVar(value="Week")
        
        self.create_widget()
        self.timer_text = self.canvas_timer.create_text(205, 40, text="25:00", font=("Helvetica", 36))
        self.timer = Timer(self.update_timer_text)
        master.protocol("WM_DELETE_WINDOW", self.on_close)

        # グラフを初期化
        self.update_graph()

    def create_widget(self):
        '''アプリケーションの画面を定義
        
        フレーム
        キャンバス
        ボックス
        ボタン
        
        '''
        # フレーム設定
        self.screen_main_menu = tk.Canvas(self.master, width=430, height=200)
        self.screen_timer = tk.Canvas(self.master, width=430, height=200)
        self.screen_input = tk.Canvas(self.master, width=600, height=100)
        self.screen_learning_data = tk.Canvas(self.master, width=1020, height=600)

        self.screen_main_menu.pack()
        
        # screen_timer画面のキャンバス
        self.canvas_timer = tk.Canvas(self.screen_timer, width=410, height=70, bg="lightblue")
        self.canvas_timer.place(x=10, y=10)
        
        # screen_learning_data画面のグラフ描画用キャンバス
        self.canvas_learning_graph = FigureCanvasTkAgg(plt.Figure(figsize=(5, 3)), master=self.screen_learning_data)
        self.canvas_task_pie = FigureCanvasTkAgg(plt.Figure(figsize=(5, 3)), master=self.screen_learning_data)
        self.learning_graph = self.canvas_learning_graph.get_tk_widget()
        self.task_pie_graph = self.canvas_task_pie.get_tk_widget()
        self.learning_graph.place(x=10, y=10, width=500, height=300)
        self.task_pie_graph.place(x=520, y=10, width=500, height=300)
        
        # 円グラフ表示期間切り替えようドロップダウンリスト
        self.period_options = ["Day", "Week", "Month", "Year"]
        self.selected_period = tk.StringVar(value=self.period_options[1])
        self.dropdown_period = ttk.Combobox(self.screen_learning_data, textvariable=self.selected_period, values=self.period_options)
        self.dropdown_period.place(x=10, y=520)
        self.dropdown_period.bind("<<ComboboxSelected>>", self.update_graph)

        # タスク名選択ボックスを作成
        '''
        更新予定
        '''
        self.dropdown_task = ttk.Combobox(self.screen_input, state='normal')
        self.dropdown_task.place(x=10, y=10)
        
        # スタイルの標準設定
        style = ttk.Style()
        style.configure("TButton",  font=("MSゴシック体", "18","bold"))
        
        # ボタンの作成
        self.button_start_timer = ttk.Button(self.screen_main_menu, text="start_timer")
        self.button_start_learning_data = ttk.Button(self.screen_main_menu, text="Leaning_data")
        
        self.button_start_stop = ttk.Button(self.screen_timer, text="start / stop")
        self.button_end = ttk.Button(self.screen_timer, text="end")
        self.button_back = ttk.Button(self.screen_timer, text="back")
        
        self.button_entry = ttk.Button(self.screen_input, text='Entry')
        
        self.button_prev_time = ttk.Button(self.screen_learning_data, text="<")
        self.button_next_time = ttk.Button(self.screen_learning_data, text=">")
        self.button_prev = ttk.Button(self.screen_learning_data, text="<")
        self.button_next = ttk.Button(self.screen_learning_data, text=">")
        self.button_change = ttk.Button(self.screen_learning_data, text="Update")

        # ボタンの配置
        self.button_start_timer.place(x=10, y=10, width=200, height=60)
        self.button_start_learning_data.place(x=220, y=10, width=200,height=60)
        
        self.button_start_stop.place(x=10, y=90, width=270, height=50)
        self.button_end.place(x=290, y=90, width=120, height=50)
        self.button_back.place(x=290, y=145, width=120, height=50)
        
        self.button_entry.place(relx=0.5, rely=0.5,anchor='center')
        
        self.button_prev_time.place(x=10, y=420, width=120, height=50)
        self.button_next_time.place(x=380, y=420, width=120, height=50)
        self.button_prev.place(x=520, y=420, width=120, height=50)
        self.button_next.place(x=890, y=420, width=120, height=50)
        self.button_change.place(x=650, y=420, width=120, height=50)
        
        # ボタンのコマンドを設定
        self.button_start_timer.config(command=self.show_timer_screen)
        self.button_start_learning_data.config(command=self.show_learning_data_screen)
        self.button_back.config(command=self.process_back)
        self.button_start_stop.config(command=self.process_start_stop)
        self.button_end.config(command=self.process_end)
        self.button_entry.config(command=self.process_entry)
        self.button_prev_time.config(command=self.process_prev_time)
        self.button_next_time.config(command=self.process_next_time)
        self.button_change.config(command=self.update_graph)

    def process_start_stop(self):
        '''start / stopボタンの処理'''
        if not self.timer.timer_running:
            self.timer.start_timer()
        else:
            self.timer.stop_timer()

    def process_end(self):
        '''endボタンの処理'''
        self.timer.stop_timer()
        self.show_input_screen()
    
    def process_back(self):
        '''backボタンの処理'''
        self.show_main_menu_screen()
    
    def process_entry(self):
        '''entryボタンの処理'''
        time = self.timer.get_count_time()
        task = self.dropdown_task.get()
        nowdate = datetime.now() - timedelta(time)
        self.db_manager.insert_data(nowdate.strftime('%Y-%m-%d'), time, task)
        
    def process_prev_time(self):
        '''prevボタンの処理'''
        self.current_week_start -= timedelta(days=7)
        self.update_graph()

    def process_next_time(self):
        '''nextボタンの処理'''
        self.current_week_start += timedelta(days=7)
        self.update_graph()
        
    def process_prev(self):
        self.period = self.selected_period.get()
        if self.period == "Day":
            self.current_week_start -= relativedelta(days=1)
        elif self.period == "Week":
            self.current_week_start -= relativedelta(weeks=1)
        elif self.period == "Month":
            self.current_week_start -= relativedelta(months=1)
        elif self.period == "Year":
            self.current_week_start -= relativedelta(years=1)
        self.update_graph()

    def process_next(self):
        self.period = self.selected_period.get()
        if self.period == "Day":
            self.current_week_start += relativedelta(days=1)
        elif self.period == "Week":
            self.current_week_start += relativedelta(weeks=1)
        elif self.period == "Month":
            self.current_week_start += relativedelta(months=1)
        elif self.period == "Year":
            self.current_week_start += relativedelta(years=1)
        self.update_graph()
        
    def update_graph(self, *args):
        self.period = self.selected_period.get()
        start_date = datetime.today()
        
        if self.period == "Day":
            end_date = start_date
        elif self.period == "Week":
            start_date -= timedelta(days=start_date.weekday())
            end_date = start_date + relativedelta(weeks=1) - relativedelta(days=1)
        elif self.period == "Month":
            start_date = start_date.replace(day=1)
            end_date = start_date + relativedelta(months=1) - relativedelta(days=1)
        elif self.period == "Year":
            start_date = start_date.replace(month=1, day=1)
            end_date = start_date + relativedelta(years=1) - relativedelta(days=1)

        # データの取得とグラフの描画
        task_data = self.db_manager.query_task_data(start_date, end_date)
        period_data = self.db_manager.query_date(start_date, end_date)
        self.draw_charts(period_data, task_data)
        
    def update_timer_text(self, time_text):
        self.canvas_timer.itemconfig(self.timer_text, text=time_text)
        if self.timer.timer_running:
            self.after(1000, self.timer.update_timer)
            
    def draw_charts(self, weekly_data, task_data):
        # 新しい Figure オブジェクトを作成
        fig = plt.Figure(figsize=(10, 4))

        # 棒グラフの追加
        ax1 = fig.add_subplot(121)
        dates = [datetime.strptime(date, '%Y-%m-%d').strftime('%m/%d') for date in weekly_data.keys()]
        times = [t / 60 for t in weekly_data.values()]
        ax1.bar(dates, times, color='blue')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Learning Time (hours)')
        ax1.set_title('Weekly Learning Time')
        ax1.set_xticklabels(dates, rotation=45)

        ax2_frame = fig.add_subplot(122)
        ax2_frame.axis('off')
        
        # 円グラフの追加
        ax2 = fig.add_subplot(122, label='pie', frame_on=False)
        ax2.set_position(ax2_frame.get_position())
        labels = [x[0] for x in task_data]
        sizes = [x[1] for x in task_data]
        ax2.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax2.axis('equal')
        ax2.set_title('Task Distribution')
        
        for _, spine in ax2_frame.spines.items():
            spine.set_visible(True)
            spine.set_edgecolor('black')
            spine.set_linewidth(2)

        # キャンバスを作成して配置
        self.canvas_charts = FigureCanvasTkAgg(fig, master=self.screen_learning_data)
        self.charts_graph = self.canvas_charts.get_tk_widget()
        self.charts_graph.place(x=10, y=10, width=1000, height=400)
        
    def update_dropdown_tasks(self):
        tasks = self.db_manager.get_tasks()
        self.dropdown_task['values'] = tasks

    def calculate_dates(self):
        # 選択された期間に基づいて日付を計算する補助関数
        if self.period == "Day":
            start_date = self.current_week_start
            end_date = self.current_week_start
        elif self.period == "Week":
            start_date = self.current_week_start
            end_date = self.current_week_start + timedelta(days=6)
        elif self.period == "Month":
            start_date = self.current_week_start
            end_date = self.current_week_start + timedelta(days=30)
        elif self.period == "Year":
            start_date = self.current_week_start
            end_date = self.current_week_start + timedelta(days=365)
        return start_date, end_date
    
    # main_menu画面への切り替え処理
    def show_main_menu_screen(self):
        self.screen_timer.pack_forget()
        self.screen_input.pack_forget()
        self.screen_learning_data.pack_forget()
        self.screen_main_menu.pack()
        self.master.title(self.TITLE_NAME_MAIN_MENU)
        self.master.geometry(self.WINDOW_SIZE_MAIN_MENU)

    # timer画面への切り替え
    def show_timer_screen(self):
        self.screen_main_menu.pack_forget()
        self.master.geometry(self.WINDOW_SIZE_TIMER)
        self.master.title(self.TITLE_NAME_TIMER)
        self.screen_timer.pack()
        self.timer.reset_timer()
    
    # input画面へ切り替え
    def show_input_screen(self):
        self.screen_timer.pack_forget()
        self.master.geometry(self.WINDOW_SIZE_INPUT)
        self.master.title(self.TITLE_NAME_INPUT)
        self.screen_input.pack()
        self.dropdown_task()
    
    #learning_data画面への切り替え
    def show_learning_data_screen(self):
        self.screen_main_menu.pack_forget()
        self.master.geometry(self.WINDOW_SIZE_LEARNING_DATA)
        self.master.title(self.TITLE_NAME_LEARNING_DATA)
        self.screen_learning_data.pack()
        
    

    def on_close(self):
        self.db_manager.close_db()
        self.master.quit()
        self.master.destroy()