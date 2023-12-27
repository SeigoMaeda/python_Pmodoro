from datetime import timedelta
import sqlite3

class DatabaseManager:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = sqlite3.connect(self.db_file)
        self.create_table()

    def create_table(self):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS timer_data (
                    id INTEGER PRIMARY KEY,
                    date TEXT,
                    time INTEGER,
                    task TEXT
                )
            ''')

    def insert_data(self, date, time, task):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO timer_data (date, time, task) VALUES (?, ?, ?)
            ''', (date, time, task))

    def query_task_data(self, start_date, end_date):
        cursor = self.conn.execute(
            "SELECT task, SUM(time) FROM timer_data WHERE date BETWEEN ? AND ? GROUP BY task",
            (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
        )
        return cursor.fetchall()
    
    def query_date(self, start_date, end_date):
        cursor = self.conn.execute(
            "SELECT date, SUM(time) FROM timer_data WHERE date BETWEEN ? AND ? GROUP BY date",
            (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
        )
        data = {row[0]: row[1] for row in cursor.fetchall()}

        # 指定された期間内の全ての日付を確認し、データがない場合は0を割り当てる
        current_date = start_date
        while current_date <= end_date:
            date_str = current_date.strftime('%Y-%m-%d')
            if date_str not in data:
                data[date_str] = 0
            current_date += timedelta(days=1)

        return data
    
    def get_tasks(self):
        cursor = self.conn.execute("SELECT DISTINCT task FROM timer_data")
        return [row[0] for row in cursor.fetchall()]
    
    
    def close_db(self):
        if self.conn:
            self.conn.close()
            self.conn = None