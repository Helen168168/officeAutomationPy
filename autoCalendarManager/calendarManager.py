from icalendar import Calendar, Event
from datetime import datetime, timedelta
import pytz
import uuid
import os
class CalendarManager:
    def __init__(self, calendar_name="My Calendar"):
        """初始化日历管理器"""
        self.calendar = Calendar()
        self.calendar.add('name', calendar_name)
        self.events = {}

    def add_event(self, summary, start, end, description="", location="", reminders=None):
        """
        添加一个新事件
        :param summary: 事件标题
        :param start: 开始时间 (datetime对象)
        :param end: 结束时间 (datetime对象)
        :param description: 事件描述 (可选)
        :param location: 事件地点 (可选)
        :param reminders: 提醒列表，如 [('email', -timedelta(days=1)), ('popup', -timedelta(minutes=30))]
        :return: 事件ID
        """
        event_id = str(uuid.uuid4())
        event = Event()
        event.add('uid', event_id)
        event.add('summary', summary)
        event.add('dtstart', start)
        event.add('dtend', end)
        event.add('dtstamp', datetime.now(pytz.utc))
        event.add('description', description)
        event.add('location', location)

        if reminders:
            for reminder_type, trigger in reminders:
                alarm = Event()
                alarm.add('action', reminder_type.upper())
                alarm.add('trigger', trigger)
                event.add_component(alarm)

        self.calendar.add_component(event)
        self.events[event_id] = event
        return event_id

    def remove_event(self, event_id):
        """根据事件ID删除事件"""
        if event_id in self.events:
            # 从日历中移除事件
            for component in self.calendar.subcomponents:
                if component.get('uid') == event_id:
                    self.calendar.subcomponents.remove(component)
                    break
            del self.events[event_id]
            return True
        return False

    def find_events(self, start_date=None, end_date=None, summary_keyword=None):
        """
        查找事件
        :param start_date: 开始日期范围 (可选)
        :param end_date: 结束日期范围 (可选)
        :param summary_keyword: 标题关键字 (可选)
        :return: 匹配的事件列表
        """
        results = []
        for event_id, event in self.events.items():
            event_start = event.get('dtstart').dt
            event_end = event.get('dtend').dt

            # 检查日期范围
            date_match = True
            if start_date and event_end < start_date:
                date_match = False
            if end_date and event_start > end_date:
                date_match = False

            # 检查关键字
            keyword_match = True
            if summary_keyword:
                summary = event.get('summary', '').lower()
                if summary_keyword.lower() not in summary:
                    keyword_match = False

            if date_match and keyword_match:
                results.append({
                    'id': event_id,
                    'summary': event.get('summary'),
                    'start': event_start,
                    'end': event_end,
                    'description': event.get('description'),
                    'location': event.get('location')
                })

        return results

    def export_to_ics(self, filename):
        """将日历导出为ICS文件"""
        with open(filename, 'wb') as f:
            f.write(self.calendar.to_ical())
        return os.path.abspath(filename)

    def import_from_ics(self, filename):
        """从ICS文件导入日历"""
        with open(filename, 'rb') as f:
            imported_cal = Calendar.from_ical(f.read())

        for component in imported_cal.subcomponents:
            if component.name == 'VEVENT':
                event_id = component.get('uid')
                self.events[event_id] = component
                self.calendar.add_component(component)

    def get_upcoming_events(self, days=7):
        """获取未来几天内的即将发生的事件"""
        now = datetime.now(pytz.utc)
        end_date = now + timedelta(days=days)
        return self.find_events(start_date=now, end_date=end_date)

