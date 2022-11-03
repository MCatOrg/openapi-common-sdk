package Common;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.HttpStatus;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.ContentType;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.util.EntityUtils;

import java.io.IOException;
import java.util.HashMap;

public class HttpHelper {




    public static String SendPost(String url, HashMap<String, String> headers, String body,HttpProfile profile) throws MCatCloudSDKException {
        HttpClient httpClient = null;
        HttpPost postMethod = null;
        HttpResponse response = null;

        httpClient = HttpClients.createDefault();

        try {
            postMethod = new HttpPost(url);//传入URL地址
//设置请求头

//            postMethod.addHeader("Content-type", "application/json; charset=utf-8");
            for (String k : headers.keySet()) {
                System.out.println("key: " + k + " value: " + headers.get(k));
                postMethod.addHeader(k,headers.get(k));
            }
            // 创建请求内容
            StringEntity entity = new StringEntity(body, ContentType.APPLICATION_JSON);
            postMethod.setEntity(entity);

            response = httpClient.execute(postMethod);//获取响应

            int statusCode = response.getStatusLine().getStatusCode();
            if (statusCode != HttpStatus.SC_OK) {

                System.out.println("HTTP请求未成功！HTTP Status Code:" + response.getStatusLine());

            }

            HttpEntity httpEntity = response.getEntity();

            String reponseContent = EntityUtils.toString(httpEntity);

            EntityUtils.consume(httpEntity);//释放资源

            System.out.println("响应内容：" + reponseContent);

            return  reponseContent;

        } catch (IOException e) {
            throw new MCatCloudSDKException(e.getMessage());
        }


    }

}
