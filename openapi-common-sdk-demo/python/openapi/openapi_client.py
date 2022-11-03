import os
import unittest

from example.openapi import credential, common_client
from example.openapi.ClientProfile import ClientProfile
from example.openapi.HttpProfile import HttpProfile
from example.openapi.mcat_sdk_exception import MCatSDKException


class MyTestCase(unittest.TestCase):
    def test_something(self):

        try:

            secrets_id = os.environ.get("MCAT_SECRET_ID")
            secrets_key = os.environ.get("MCAT_SECRET_KEY")
            cred = credential.Credential(
                secrets_id,
                secrets_key)

            print("key: ",secrets_key," secrets_id: ",secrets_id)


            # httpProfile = HttpProfile(protocol="http",reqMethod="GET")

            httpProfile = HttpProfile(protocol="http", reqMethod="POST")
            # HmacSHA256

            profile = ClientProfile("hmac-sha256",httpProfile,'zh-CN')

            # 实例化要请求的common client对象，clientProfile是可选的。
            client = common_client.CommonClient( cred, "ap-guangzhou",profile)

            headers = {
                # "jwt_token":"eyJ1cm5hIjoi6aqG5Lq_55S3IiwidXJpZCI6IjEyMzQ1MDA0NjY1OTgiLCJ0dGlkIjoiMTAwMDMiLCJ1c3RlIjoiMSIsInJvbGUiOlsiMiIsIjEwMTAiLCIxMDQyIl0sIm1pZHMiOlsiMjAzMCIsIjIwMjAiLCIyMDQxIiwiMTAwMSIsIjIwNjgiLCIyMDcwIiwiMjA5NiIsIjIwMjYiLCIyMTM0IiwiMjAxMiIsIjEwMTEiLCIyMTAxIiwiMTAxOCIsIjEwMDYiLCIxMDA3IiwiMTAxMCIsIjEwMTciLCIxMDA0IiwiMjAxNiIsIjIwMjciLCIyMDMyIiwiMTAwOCIsIjIwNDMiLCIyMDYwIiwiMjA4OCIsIjEwNTUiLCIyMDMxIiwiMjA2NiIsIjIwOTIiLCIyMDkwIiwiMjEwMCIsIjIxMjQiLCIyMTIyIl0sInVyZGEiOiJ7XG4gIFwidXNlcl9pZFwiOiAxMjM0NTAwNDY2NTk4LFxuICBcImNvdW50cnlfY29kZVwiOiBcIjg2XCIsXG4gIFwibW9iaWxlXCI6IFwiMTg3NTc1Nzg5MzRcIixcbiAgXCJuYW1lXCI6IFwi6aqG5Lq_55S3XCIsXG4gIFwiYWdlbnRfc3RhdHVzXCI6IDIsXG4gIFwibGV2ZWxfaWRcIjogMixcbiAgXCJjaGFubmVsX2xldmVsX2lkXCI6IDQ2XG59IiwidG9pZCI6Im9kZTgzNWRKTFFReDdmZ1dvUG9KY0RIVGJtRWMiLCJ0YXBwaWQiOiJ3eGNjODY2ZmEyYTk0MTE3N2QiLCJhcHBpZCI6IjEwMTEwMDAwMyIsImRwaWQiOiIiLCJibWlkIjoiMTAwMDMiLCJkbWlkIjoiMjAwMTQiLCJkbXJpIjoiMjAwMTQiLCJuYmYiOjE2NjYyNTI0MjcsImV4cCI6MTY2NjU0MDQyNywiaWF0IjoxNjY2MjUyNDI3fQ.DbS-4072IkO8Wl5nU1r5oIESKkqUTrk7QKWJmrrkKknKGfxGT1QhFMwmrZ8RwskKMe6-fvfPJbYxxTUNAz3lCwWpjPax63BnRFD9rEtPXx1KbK8M7rv74cYXlC7nLCd_VFjpzMQZ6_1gdwJ8NdXI6M-fvtNNW3ZhZD0NxitO5srp1DENvtpaME2M-usJ23bqIoMiOOuMYXJNjfftiC_b5-Cu4txDWPF1HFIXXqqnseNuIJudfeFvd9FN4W_sWjRu1OlgSyeQOuv1UPO9Qye3_pFqEf8_3spA8uE5ZNWCeyCiT26n7dkbtelykZXhioDTeNukln2halY0zcW4FmofoA"

            }
            options = {}
            json = {
  "UserName": "maco",
  "Code": "10009"
}

            url = "/swagger/api/OpenApi/TestGetUser"
            url = "/open/swagger/index.html"
            url = "/swagger/index.html"
            # url = "/swagger/common/v1/swagger.json"
            url = "/swagger/"

            url = "/open/openapi/api/OpenApi/TestGetUser"
            # 接口参数作为headers json字典传入，二进制数据作为body字节传入
            # 得到的输出是json字典，请求失败将抛出异常
            print(client.call_json(url,json,headers, options))
        except MCatSDKException as err:
            print(err)



if __name__ == '__main__':
    unittest.main()
