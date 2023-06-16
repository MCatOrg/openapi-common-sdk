package Common;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;

import java.lang.reflect.Type;
import java.util.HashMap;

    public class MCatClient {
        public static final int HTTP_RSP_OK = 200;
        public final String SDK_VERSION = "MCatCloud_v1.0.0";

        public Gson gson;

        public MCatClient(Credential credential, String region, ClientProfile profile) throws MCatCloudSDKException {
            this.credential = credential;
            this.profile = profile;
            this.region = region;
            this.sdkVersion = SDK_VERSION;
            this.apiVersion = "";
            gson = new Gson();

        }

        /// <summary>
        /// Credentials.
        /// </summary>
        private Credential credential;

        /// <summary>
        /// Client profiles.
        /// </summary>
        private ClientProfile profile;

        /// <summary>
        /// Service region, such as ap-guangzhou.
        /// </summary>
        private String region;

        /// <summary>
        /// SDK version.
        /// </summary>
        private String sdkVersion;

        /// <summary>
        /// API version.
        /// </summary>
        private String apiVersion;


        public Credential getCredential() {
            return credential;
        }

        public void setCredential(Credential credential) {
            this.credential = credential;
        }

        public ClientProfile getProfile() {
            return profile;
        }

        public void setProfile(ClientProfile profile) {
            this.profile = profile;
        }

        public String getRegion() {
            return region;
        }

        public void setRegion(String region) {
            this.region = region;
        }

        public String getSdkVersion() {
            return sdkVersion;
        }

        public void setSdkVersion(String sdkVersion) {
            this.sdkVersion = sdkVersion;
        }

        public String getApiVersion() {
            return apiVersion;
        }

        public void setApiVersion(String apiVersion) {
            this.apiVersion = apiVersion;
        }

        public <T> T Request(String path, String requestPayload, String contentType) throws MCatCloudSDKException {
            if (contentType == null) {
                contentType = "application/json;";
            }

            HashMap<String, String> headers = this.BuildHeaders(path, contentType, requestPayload);

            String endpoint = headers.get("Host");
            String baseUrl =  this.profile.httpProfile.getProtocol()+endpoint;

            String fullurl = baseUrl+path;
            T resp = null;
            try {
                String respbody = HttpHelper.SendPost(fullurl,headers,  requestPayload, this.profile.httpProfile);

                Type respType = new TypeToken<T>() {}.getType();
                resp = gson.fromJson(respbody, respType);

                return resp;
            } catch (Exception e) {
                throw new MCatCloudSDKException("The request with exception "+e.getMessage());
            }
        }

        private HashMap<String, String> BuildHeaders(String url, String contentType, String requestPayload) throws MCatCloudSDKException {
            String endpoint = this.profile.httpProfile.getEndpoint();

            String httpRequestMethod = this.profile.httpProfile.getReqMethod();

            String signedHeaders = "content-type;host";

            long timestamp = System.currentTimeMillis() / 1000;
            String requestTimestamp = String.valueOf(timestamp);


            String canonical_uri = url;
            String canonical_querystring = "";
            String user_key = this.credential.getSecretId();
           //没有自动补0
            // String payload_hash = SignHelper.getMD5Str(requestPayload);
            //MD5Encrypt2
            String payload_hash = SignHelper.MD5Encrypt2(requestPayload);
            String canonical_headers = "content-type:" + contentType + "\n" + "host:" + endpoint;


            // method  canonical_uri canonical_querystring user_key timestamp payload_hash canonical_headers
            String string2sign =  httpRequestMethod+
                    "\n" +
                    canonical_uri
                    +"\n"
                    +canonical_querystring
                    +"\n"
                    +user_key
                    +"\n"
                    +requestTimestamp
                    +"\n"
                    +payload_hash
                    +"\n" +
                    canonical_headers;
            System.out.println("string2sign:"+ string2sign);
            System.out.println("requestPayload:"+requestPayload);
            String signature = SignHelper.Sign(credential.getSecretKey(), string2sign, profile.signMethod);

            System.out.println("signature:"+ signature);
            //'Authorization: hmac-auth-v1# + ACCESS_KEY + # + SIGNATURE + # + ALGORITHM + # + DATE + # + SIGNED_HEADERS'

            String authorization =
                    "hmac-auth-v1#" + credential.getSecretId() + "#" + signature + "#" + profile.signMethod + "#" + requestTimestamp + "#" + signedHeaders;

            System.out.println("authorization:"+ authorization);

            HashMap<String, String> headers = new HashMap<String, String>();
            headers.put("Authorization", authorization);
            headers.put("Host", endpoint);
            headers.put("Content-Type", contentType);
            headers.put("X-MT-Timestamp", requestTimestamp);
            headers.put("X-MT-Version", this.apiVersion);

            if (this.credential.getToken() != null) {
                headers.put("X-MT-Token", this.credential.getToken());
            }

            return headers;
        }


    }
