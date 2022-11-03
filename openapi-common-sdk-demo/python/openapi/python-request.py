import json
import time
import hashlib

import md5hash as md5hash
import requests

rid = 'zhoujt_test'
user = 'zhoujiangtao'
token = 'xxxxxxxxxxxxx'
nowtime = int(time.time())
signstr = user + str(nowtime) + rid + token
signature = ""

headers = {
    'User': user,
    'Timestamp': str(nowtime),
    'cc_request_id': rid,
    'Authorization': signature,
    'Content-Type': 'application/json'
}
# 查询
list_url = "http://openapi.r.b2co.cn/api/OpenApi/TestGetUser"

# 查看data
data = {"UserName": "maco", "Code": "10009"}

res = requests.request("POST", url=list_url, data=json.dumps(data), headers=headers)
print(res.json())