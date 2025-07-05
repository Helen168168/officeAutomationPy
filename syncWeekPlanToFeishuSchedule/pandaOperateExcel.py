import os
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Union

class ExcelOperation:
    def __init__(self, path: str = ""):
        self.path = path
        self.all_sheets_data: Dict[str, pd.DataFrame] = {}
        self.all_sheet_names: List[str] = []
        
    def is_file_path_valid(self) -> bool:
        """检查文件是否存在"""
        if not os.path.exists(self.path):
            raise FileNotFoundError(f"文件不存在: {self.path}")
        return True
    
    def load_all_sheets(self) -> None:
        """读取Excel所有sheet数据到DataFrame"""
        if not self.is_file_path_valid():
            return
            
        with pd.ExcelFile(self.path) as excel:
            self.all_sheet_names = excel.sheet_names
            self.all_sheets_data = {
                sheet_name: pd.read_excel(excel, sheet_name=sheet_name, header=None)
                for sheet_name in self.all_sheet_names
            }
    
    def get_all_week_plan_info(self) -> Dict[str, Dict[str, List[str]]]:
        """获取所有sheet的周计划信息"""
        all_cell_content = {}
        
        for sheet_name, df in self.all_sheets_data.items():
            week_name = df.iat[0, 0] if pd.notna(df.iat[0, 0]) else ""
            if "周计划" not in str(week_name):
                continue
                
            week_data = {}
            current_day = None
            
            for _, row in df.iterrows():
                for cell in row:
                    if pd.isna(cell):
                        continue
                        
                    cell_str = str(cell)
                    if cell_str in ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]:
                        current_day = cell_str
                        week_data[current_day] = []
                    elif current_day:
                        week_data[current_day].append(cell_str)
            
            if week_name and week_data:
                all_cell_content[week_name] = week_data
                
        return all_cell_content
    
    @staticmethod
    def split_date(date_str: str) -> str:
        """日期切割"""
        if pd.isna(date_str) or not date_str:
            return ""
        return str(date_str).split("-")[0]
    
    @staticmethod
    def split_time_plan(date: datetime.date, plan: str) -> List[Dict[str, Union[datetime.datetime, str]]]:
        """将时间计划字符串解析为结构化数据"""
        time_plan = []
        
        if pd.isna(plan) or not plan:
            return time_plan
            
        for time_entry in str(plan).split("\n\n"):
            parts = time_entry.split(" ")
            if not parts:
                continue
                
            # 处理时间部分
            time_parts = parts[0].split("-")
            if len(time_parts) != 2:
                continue
                
            start_time = datetime.combine(
                date, 
                datetime.strptime(time_parts[0], "%H:%M").time()
            )
            end_time = datetime.combine(
                date,
                datetime.strptime(time_parts[1], "%H:%M").time()
            )
            
            # 处理内容部分
            content = " ".join(parts[1:]) if len(parts) > 1 else ""
            
            time_plan.append({
                "startTime": start_time,
                "endTime": end_time,
                "content": content
            })
            
        return time_plan
    
    def split_schedule_info(self) -> Tuple[List[List[Dict]], List[str]]:
        """
        获取所有的日程计划和日程执行的反馈信息
        返回: (日程计划列表, 反馈信息列表)
        """
        schedule_info = []
        feedback_info = []
        all_cell_content = self.get_all_week_plan_info()
        
        for week_name, week_data in all_cell_content.items():
            start_week_date = self.split_date(week_name)
            if not start_week_date:
                continue
                
            base_date = datetime.strptime(start_week_date, "%Y/%m/%d").date()
            
            for day_idx, (day_name, day_plans) in enumerate(week_data.items()):
                if not day_plans:
                    continue
                    
                current_date = base_date + timedelta(days=day_idx)
                
                # 第一个元素是日程计划
                if day_plans[0]:
                    schedule_info.extend(
                        self.split_time_plan(current_date, day_plans[0])
                    )
                
                # 其余元素是反馈信息
                for feedback in day_plans[1:]:
                    if pd.notna(feedback) and feedback:
                        feedback_info.append(str(feedback))
                        
        return schedule_info, feedback_info

excel_op = ExcelOperation("path/to/your/file.xlsx")
excel_op.load_all_sheets()
schedules, feedbacks = excel_op.split_schedule_info()

# 打印结果
print("日程计划:")
for schedule in schedules:
    print(schedule)

print("\n反馈信息:")
for feedback in feedbacks:
    print(feedback)