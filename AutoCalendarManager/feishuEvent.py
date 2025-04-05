'''
1. 在飞书开放平台的企业自建应用，申请以下权限：
calendar:calendar:readonly（读日历）
calendar:calendar:write（写日历）
calendar:event:readonly（读日程）
calendar:event:write（写日程）
2. 获取访问凭证
3.同步日程
# 安装SDK pip install lark-oapi
'''

import json
from calendarId import getCalendarInfo
from officeAutomationPy.baseModule.request import Request
from officeAutomationPy.baseModule.cacheData import GlobalCache
cache = GlobalCache()

class ScheduleManager:
    def __init__(self, calendarId='', event={}):
        self.calendarId = calendarId
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f'Bearer {cache["tenant_access_token"]}'
        }
        self.params= {
            "user_id_type": 'user_id',
        }
        self.event = {
              "summary": "日程标题",
              "description": "日程描述",
              "start_time": {
                "date": "2025-04-08",

                "timezone": "Asia/Shanghai"
              },
              "end_time": {
                "date": "2025-04-09",
                "timezone": "Asia/Shanghai"
              }
        }

    def ceateEvent(self):
        # 创建事件
        url = f'https://open.feishu.cn/open-apis/calendar/v4/calendars/{self.calendarId}/events'
        result = Request(url=url, method='POST', headers=self.headers, data=self.event).send()
        if result.get("code") == 0:
            print("新增成功")
        else:
            print(f"失败")

    def updateEvent(self):
        event_id = 'eb4b317f-0fa7-4f9f-ab3c-8d2c288d9120_0'
        self.event = {
            "summary": "更新日程",
            "description": "周计划",
            "start_time": {
                "date": "2025-04-09",
                "timezone": "Asia/Shanghai"
            },
            "end_time": {
                "date": "2025-04-10",
                "timezone": "Asia/Shanghai"
            }
        }

        # 更新事件
        url = f'https://open.feishu.cn/open-apis/calendar/v4/calendars/{self.calendarId}/events/{event_id}'
        result = Request(url=url, method='PATCH', headers=self.headers).send()
        if result.get("code") == 0:
            print("修改成功")
        else:
            print(f"失败")

    def deleteEvent(self):
        event_id = 'eb4b317f-0fa7-4f9f-ab3c-8d2c288d9120_0'
        # 删除事件
        url = f'https://open.feishu.cn/open-apis/calendar/v4/calendars/{self.calendarId}/{event_id}'
        Request(url=url, method='DELETE', headers=self.headers).send()
        print('删除成功!')

    def getScheduleList(self):
        # 获取事件
        url = f'https://open.feishu.cn/open-apis/calendar/v4/calendars/{self.calendarId}/events'
        scheduleList = Request(url=url, method='GET', headers=self.headers).send()
        print(f"获取日程列表成功: {scheduleList}")
        return scheduleList

def getCalendarId():
    calendarInfo = getCalendarInfo()
    for calendar in calendarInfo:
        calendar_id = calendar['calendar']['calendar_id']
        user_id = calendar['user_id']
        if calendar_id:
            print(f"日历ID: {calendar_id}")
            cache['calendar_id'] = calendar_id
            cache['user_id'] = user_id
            print(f"user_id: {user_id}")
            return calendar_id

calendarId = getCalendarId()
scheduleManager = ScheduleManager(calendarId=calendarId)
scheduleManager.ceateEvent()
scheduleManager.getScheduleList()
scheduleManager.updateEvent()
scheduleManager.deleteEvent()