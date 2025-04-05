import pandas as pd
import sqlite3
import json

class DataLoader:
    @staticmethod
    def load_csv(filepath):
        """ 从CSV文件加载数据 """
        return pd.read_csv(filepath)

    @staticmethod
    def load_excel(filepath, sheet_name=0):
        """从Excel文件加载数据"""
        return pd.read_excel(filepath, sheet_name=sheet_name)

    @staticmethod
    def load_json(filepath):
        """ 从JSON文件加载数据 """
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

    # @staticmethod
    # def load_sqlite(db_path, query):
    #     """从SQLite数据库加载数据"""
    #     conn = sqlite3.connect(db_path)
    #     return pd.read_sql(query, conn)