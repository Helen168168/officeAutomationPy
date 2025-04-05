'''
获取飞书的应用和用户Token
'''

from officeAutomationPy.baseModule.request import Request
from officeAutomationPy.baseModule.cacheData import GlobalCache
cache = GlobalCache()
app_id = "" # 自建应用ID
app_secret = "" # 自建应用密钥
headers = {"Content-Type": "application/json"}
data = {
    "app_id": app_id,
     "app_secret": app_secret
}

# 获取自建应用ID
def getTenantAccessToken():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    result = Request(url=url, method='POST', headers=headers, data=data).send()
    if result.get("code") == 0:
        tenant_access_token = result["tenant_access_token"]
        print(f"获取成功tenant_access_token: {tenant_access_token}")
        print(f"过期时间: {result['expire']}秒")  # 通常为7200秒(2小时)
        cache["tenant_access_token"] = tenant_access_token  # 设置值

        return tenant_access_token
    else:
        print(f"失败: {result.get('msg')}")


# 自建应用的Token
def getAppAccessToken():
    url = "https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal"
    result = Request(url=url, method='POST', headers=headers, data=data).send()
    if result.get("code") == 0:
        app_access_token = result["app_access_token"]
        tenant_access_token = result["tenant_access_token"]
        print(f"获取成功app_access_token: {app_access_token}")
        print(f"过期时间: {result['expire']}秒")
        cache["app_access_token"] = app_access_token
        cache["tenant_access_token"] = tenant_access_token
        return  (app_access_token, tenant_access_token)
    else:
        print(f"失败: {result.get('msg')}")

# 获取用户Token
def getUserAccessToken():
    url = "https://open.feishu.cn/open-apis/authen/v2/oauth/token"
    data = {
        "grant_type": "authorization_code",
        "client_id": app_id,
        "client_secret": app_secret,
        "code": "",
        "redirect_uri": f"https://open.feishu.cn/app/{app_id}/baseinfo",
        "code_verifier": "TxYmzM4PHLBlqm5NtnCmwxMH8mFlRWl_ipie3O0aVzo"
    }
    data.code = getCodeForUserInfo() # 获取授权码

    result = Request(url=url, method='POST', headers=headers, data=data).send()
    if result.get("code") == 0:
        user_access_token = result["access_token"]
        print(f"获取成功tenant_access_token: {user_access_token}")
        print(f"过期时间: {result['expire']}秒")  # 通常为7200秒(2小时)
        cache["user_access_token"] = user_access_token
        return user_access_token
    else:
        print(f"失败: {result.get('msg')}")

# 获取授权码
def getCodeForUserInfo():
    # Build authorization URL with required parameters
    auth_url = "https://open.feishu.cn/open-apis/authen/v1/authorize"
    params = {
        "app_id": app_id,
        "redirect_uri": f"https://open.feishu.cn/app/{app_id}/baseinfo",
        "response_type": "code"
    }
    # Print the URL that user needs to visit
    auth_link = f"{auth_url}?{'&'.join(f'{k}={v}' for k, v in params.items())}"
    result = Request(url=auth_link).send()
    if result.status_code == 200:
        # 将响应解析为JSON字典
        data = result.json()
        code = data["code"]
        print(f"获取成功code: {code}")
        print(f"过期时间: {result['expire']}秒")
        return code
    else:
        print(f"失败: {result.get('msg')}")
