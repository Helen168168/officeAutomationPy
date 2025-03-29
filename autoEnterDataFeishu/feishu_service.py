import requests
import logging
from typing import List, Dict
from officeAutomationPy.autoEnterDataFeishu.config import Config

class FeishuService:
    def __init__(self):
        self.base_url = "https://open.feishu.cn/open-apis"
        self.token = self._get_access_token()

    def _get_access_token(self) -> str:
        """获取飞书API访问令牌"""
        url = f"{self.base_url}/auth/v3/tenant_access_token/internal"
        headers = {"Content-Type": "application/json"}
        payload = {
            "app_id": Config.FEISHU_APP_ID,
            "app_secret": Config.FEISHU_APP_SECRET
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json().get("tenant_access_token")
        except Exception as e:
            logging.error(f"获取飞书token失败: {str(e)}")
            raise

    def upload_to_feishu(self, data: List[Dict]) -> bool:
        """批量写入飞书多维表格"""
        url = f"{self.base_url}/bitable/v1/apps/{Config.FEISHU_SHEET_TOKEN}/tables/{Config.FEISHU_TABLE_ID}/records/batch_create"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        payload = {"records": [{"fields": item} for item in data]}

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            logging.info(f"成功写入{len(data)}条数据到飞书")
            return True
        except Exception as e:
            logging.error(f"飞书数据写入失败: {str(e)}")
            return False

    def clear_table(self):
        """清空现有数据（可选）"""
        # 实现先查询再删除的逻辑（飞书API需要分步操作）
        pass