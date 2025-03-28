import pandas as pd
import logging
from datetime import datetime
from pydantic import BaseModel, ValidationError
from config import Config
from feishu_service import FeishuService
from typing import List, Dict

class ProductRecord(BaseModel):
    product_id: str
    name: str
    category: str
    price: float
    stock: int
    last_updated: datetime


class DataProcessor:
    def __init__(self):
        self.logger = self._setup_logging()
        self.feishu = FeishuService()

    def _setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(Config.LOG_FILE),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)

    def load_data(self) -> pd.DataFrame:
        """加载CSV数据"""
        try:
            df = pd.read_csv(Config.INPUT_CSV, parse_dates=['last_updated'])
            self.logger.info(f"成功加载数据，共 {len(df)} 条记录")
            return df
        except Exception as e:
            self.logger.error(f"数据加载失败: {str(e)}")
            raise

    def clean_data(self, raw_data: pd.DataFrame) -> pd.DataFrame:
        """数据清洗和验证"""
        try:
            # 基础清洗
            df = raw_data.copy()
            df = df.dropna(subset=['product_id']).drop_duplicates()

            # 数据校验
            valid_data = []
            for _, row in df.iterrows():
                try:
                    record = ProductRecord(**row.to_dict())
                    valid_data.append(row)
                except ValidationError as e:
                    self.logger.warning(f"无效数据: {row.to_dict()} | 错误: {str(e)}")

            return pd.DataFrame(valid_data)
        except Exception as e:
            self.logger.error(f"数据清洗失败: {str(e)}")
            raise

    def process_data(self, clean_data: pd.DataFrame) -> List[Dict]:
        """转换为飞书API所需格式"""
        return [{
            "产品ID": row['product_id'],
            "产品名称": row['name'],
            "分类": row['category'],
            "价格": float(row['price']),
            "库存": int(row['stock']),
            "更新时间": row['last_updated'].strftime('%Y-%m-%d %H:%M:%S')
        } for _, row in clean_data.iterrows()]

    def run_pipeline(self, output_type: str = "feishu"):
        """主处理流程"""
        try:
            self.logger.info("=== 开始数据处理 ===")

            # 数据加载与清洗
            raw_data = self.load_data()
            clean_data = self.clean_data(raw_data)

            # 飞书数据写入
            if output_type == "feishu":
                feishu_data = self.process_data(clean_data)
                self.feishu.upload_to_feishu(feishu_data)
            else:
                raise ValueError("不支持的输出类型")

            self.logger.info("=== 处理完成 ===")
            return True
        except Exception as e:
            self.logger.critical(f"流程执行失败: {str(e)}")
            return False