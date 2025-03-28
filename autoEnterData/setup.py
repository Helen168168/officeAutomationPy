import pandas as pd
from config import Config

def generate_sample_csv():
    """生成示例CSV文件"""
    sample_data = {
        "product_id": ["P1001", "P1002", "P1003"],
        "name": ["产品A", "产品B", "产品C"],
        "category": ["电子", "家居", "食品"],
        "price": [299.99, 149.50, 15.80],
        "stock": [45, 120, 89],
        "last_updated": ["2023-01-01 00:00:00", "2023-01-02 00:00:00", "2023-01-03 00:00:00"]
    }
    pd.DataFrame(sample_data).to_csv(Config.INPUT_CSV, index=False)
    print(f"示例CSV已生成: {Config.INPUT_CSV}")


generate_sample_csv()