package Common;

public class TestClient {

    public static void main(String [] args) {
        try{
            // 必要步骤：
            // 实例化一个认证对象，入参需要传入 密钥对secretId，secretKey。
            // 这里采用的是从环境变量读取的方式，需要在环境变量中先设置这两个值。
            // 你也可以直接在代码中写死密钥对，但是小心不要将代码复制、上传或者分享给他人，
            // 以免泄露密钥对危及你的财产安全。
            Credential cred = new Credential(

                  System.getenv("MCAT_SECRET_ID"),
                    System.getenv("MCAT_SECRET_KEY")
            );


            // 非必要步骤
            // 实例化一个客户端配置对象，可以指定超时时间等配置
            //HttpProfile httpProfile = new HttpProfile("openapi.r.b2co.cn", HttpProfile.REQ_HTTP);
            HttpProfile httpProfile = new HttpProfile("local-openapi.b2co.cn", HttpProfile.REQ_HTTP);
//            HttpProfile httpProfile = new HttpProfile("openapi.r.b2co.cn", HttpProfile.REQ_HTTP);

            var clientProfile = new ClientProfile("hmac-sha256", httpProfile);

            MCatClient client = new MCatClient(cred, "ap-guangzhou", clientProfile);


            //string url = "/open/openapi/api/OpenApi/TestGetUser";
            String url = "/open/openapi/api/wbc/read/integral/shopping/user/get";


            String json = "{\"Data\":{\"filters\":{\"rules\":[{\"data\":\"string\",\"field\":\"string\",\"op\":\"string\"}]},\"order\":\"string\",\"page\":0,\"rows\":0}}";


            var strResp = client.Request(url,json,"application/json") ;
            // 输出返回的字符串结果
            System.out.println(strResp);
        } catch (MCatCloudSDKException e) {
            System.out.println(e.toString());
        }
    }

}
