using MCatCloud.Common;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using Newtonsoft.Json;
using System;
using System.Net;

namespace TestProject1
{


    public class TestUser { 
       public string UserName { get; set; }
        public string Code { get; set; }
    }

    [TestClass]
    public class UnitTest1
    {
        [TestMethod]
        public void TestMethod1()
        {

            try
            {
                // 必要步骤：
                // 实例化一个认证对象，入参需要传入 密钥对secretId，secretKey。
                // 这里采用的是从环境变量读取的方式，需要在环境变量中先设置这两个值。
                // 你也可以直接在代码中写死密钥对，但是小心不要将代码复制、上传或者分享给他人，
                // 以免泄露密钥对危及你的财产安全。
                Credential cred = new Credential
                {
                    SecretId = Environment.GetEnvironmentVariable("MCAT_SECRET_ID"),
                    SecretKey = Environment.GetEnvironmentVariable("MCAT_SECRET_KEY")
                };

                // 实例化一个client选项，可选的，没有特殊需求可以跳过
                ClientProfile clientProfile = new ClientProfile();
                // 非必要步骤
                // 实例化一个客户端配置对象，可以指定超时时间等配置
                //HttpProfile httpProfile = new HttpProfile("openapi.r.b2co.cn", HttpProfile.REQ_HTTP);
                HttpProfile httpProfile = new HttpProfile("local-openapi.b2co.cn", HttpProfile.REQ_HTTP);
                // 代理服务器，当你的环境下有代理服务器时设定
                httpProfile.WebProxy = Environment.GetEnvironmentVariable("HTTPS_PROXY");

                clientProfile.HttpProfile = httpProfile;

                var profile = new ClientProfile("hmac-sha256", httpProfile); 
                 
                MCatClient client = new MCatClient(cred, "ap-guangzhou", clientProfile);

       
               //string url = "/open/openapi/api/OpenApi/TestGetUser";
                string url = "/open/openapi/api/wbc/read/integral/shopping/user/get";


                var user = new TestUser {
                     Code="10009",
                     UserName = "maco"
                };
                string json = JsonConvert.SerializeObject(user);
                json = "{\"Data\":{\"filters\":{\"rules\":[{\"data\":\"string\",\"field\":\"string\",\"op\":\"string\"}]},\"order\":\"string\",\"page\":0,\"rows\":0}}";


                var strResp = client.Request<InfoData<TestUser>>(url, json); 

                // 输出json格式的字符串回包
                Console.WriteLine(JsonConvert.SerializeObject(strResp));
            }
            catch (Exception e)
            {
                Console.WriteLine(e.ToString());
            }

        }
    }
}
