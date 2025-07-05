'''
日历管理：自动化日程安排和日历更新
从源头文件获取日程信息，经过Python的处理，自动同步到飞书日历中
'''

from datetime import datetime, timedelta
import pytz
from calendarManager import CalendarManager

# 创建日历管理器
cm = CalendarManager("工作日程")

# 添加几个事件
now = datetime.now(pytz.utc)

# 会议事件
meeting_id = cm.add_event(
    summary="项目进度会议",
    start=now + timedelta(hours=2),
    end=now + timedelta(hours=3),
    description="讨论项目当前进度和下一步计划",
    location="会议室A",
    reminders=[('popup', timedelta(minutes=-30))]
)

# 午餐事件
lunch_id = cm.add_event(
    summary="午餐时间",
    start=now + timedelta(days=1, hours=12),
    end=now + timedelta(days=1, hours=13),
    description="记得按时吃午餐"
)

# 查找事件
print("所有事件:")
for event in cm.find_events():
    print(f"{event['start']} - {event['end']}: {event['summary']}")

print("\n未来7天内的事件:")
for event in cm.get_upcoming_events(7):
    print(f"{event['start']} - {event['end']}: {event['summary']}")

# 导出日历
ics_file = cm.export_to_ics("my_calendar.ics")
print(f"\n日历已导出到: {ics_file}")

# 删除一个事件
cm.remove_event(lunch_id)
print("\n删除午餐事件后剩余事件:")
for event in cm.find_events():
    print(f"{event['start']} - {event['end']}: {event['summary']}")