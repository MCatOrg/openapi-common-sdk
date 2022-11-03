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
                // ��Ҫ���裺
                // ʵ����һ����֤���������Ҫ���� ��Կ��secretId��secretKey��
                // ������õ��Ǵӻ���������ȡ�ķ�ʽ����Ҫ�ڻ���������������������ֵ��
                // ��Ҳ����ֱ���ڴ�����д����Կ�ԣ�����С�Ĳ�Ҫ�����븴�ơ��ϴ����߷�������ˣ�
                // ����й¶��Կ��Σ����ĲƲ���ȫ��
                Credential cred = new Credential
                {
                    SecretId = Environment.GetEnvironmentVariable("MCAT_SECRET_ID"),
                    SecretKey = Environment.GetEnvironmentVariable("MCAT_SECRET_KEY")
                };

                // ʵ����һ��clientѡ���ѡ�ģ�û�����������������
                ClientProfile clientProfile = new ClientProfile();
                // �Ǳ�Ҫ����
                // ʵ����һ���ͻ������ö��󣬿���ָ����ʱʱ�������
                //HttpProfile httpProfile = new HttpProfile("openapi.r.b2co.cn", HttpProfile.REQ_HTTP);
                HttpProfile httpProfile = new HttpProfile("local-openapi.b2co.cn", HttpProfile.REQ_HTTP);
                // ���������������Ļ������д��������ʱ�趨
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

                // ���json��ʽ���ַ����ذ�
                Console.WriteLine(JsonConvert.SerializeObject(strResp));
            }
            catch (Exception e)
            {
                Console.WriteLine(e.ToString());
            }

        }
    }
}
