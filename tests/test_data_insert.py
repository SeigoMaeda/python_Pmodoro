import sys
import os
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)

from app.db_manager import DatabaseManager
from datetime import datetime, timedelta

class TestInsert:
    def __init__(self, db_file):
        self.db_manager = DatabaseManager(db_file)

    def insert_test_data(self):
        # テストデータの挿入
        for i in range(10):  # 10日分のデータを挿入
            date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            time = i * 30  # 仮の学習時間
            task = f'Test Task {i}'
            self.db_manager.insert_data(date, time, task)

        print("Test data inserted successfully.")

    def close(self):
        # データベースを閉じる
        self.db_manager.close_db()


if __name__ == "__main__":
    test_inserter = TestInsert("learning_data")
    test_inserter.insert_test_data()
    test_inserter.close()