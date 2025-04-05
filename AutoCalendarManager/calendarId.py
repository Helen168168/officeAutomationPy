'''
获取日历ID
'''
import asyncio
from officeAutomationPy.baseModule.request import Request
from getAccessToken import getTenantAccessToken

calendarInfos = {}

# 获取自建应用ID
def getCalendarInfo():
    tenant_access_token = getTenantAccessToken()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f'Bearer {tenant_access_token}'
    }
    data = {
        "user_id_type": 'open_id'
    }
    url = "https://open.feishu.cn/open-apis/calendar/v4/calendars/primary"
    result = Request(url=url, method='POST', headers=headers, data=data).send()
    if result.get("code") == 0:
        calendarInfo = result["data"]["calendars"]
        print(f"获取成功: {calendarInfo}")
        return calendarInfo
    else:
        print(f"失败: {result.get('msg')}")


