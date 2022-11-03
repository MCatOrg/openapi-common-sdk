using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;

namespace MCatCloud.Common
{
    public class MCatClient
    {
        public const int HTTP_RSP_OK = 200;
        public const string SDK_VERSION = "MCatCloud_v1.0.0";

        public MCatClient( Credential credential, string region, ClientProfile profile)
        {
            this.Credential = credential;
            this.Profile = profile; 
            this.Region = region; 
            this.SdkVersion = SDK_VERSION;
            this.ApiVersion = "";
            
        }

        /// <summary>
        /// Credentials.
        /// </summary>
        public Credential Credential { get; set; }

        /// <summary>
        /// Client profiles.
        /// </summary>
        public ClientProfile Profile { get; set; } 

        /// <summary>
        /// Service region, such as ap-guangzhou.
        /// </summary>
        public string Region { get; set; } 

        /// <summary>
        /// SDK version.
        /// </summary>
        public string SdkVersion { get; set; }

        /// <summary>
        /// API version.
        /// </summary>
        public string ApiVersion { get; set; }  

     

 

        public  T    Request<T>(string path, string requestPayload, string contentType= "application/json")
        {
             


            Dictionary<string, string> headers = this.BuildHeaders(path,contentType, requestPayload);
   
            string endpoint = headers["Host"];
            string baseUrl = $"{this.Profile.HttpProfile.Protocol}{endpoint}";

            string fullurl = $"{baseUrl.TrimEnd('/')}{path}";

      
            try
            {
              string json =  HttpHelper.PostWebRequest(fullurl, requestPayload, headers, contentType);
              T obj =  JsonConvert.DeserializeObject<T>(json);
              return obj;
            }
            catch (Exception e)
            {
                throw new MCatCloudSDKException($"The request with exception: {e.Message}");
            }
        }

        private Dictionary<string, string> BuildHeaders(string url,string contentType, string requestPayload)
        {
            string endpoint = this.Profile.HttpProfile.Endpoint;
         
            string httpRequestMethod = this.Profile.HttpProfile.ReqMethod;
        
            string signedHeaders = "content-type;host"; 
             
            long timestamp = ToTimestamp() / 1000;
            string requestTimestamp = timestamp.ToString();
           

            string canonical_uri = url;
            string canonical_querystring = "";
            string user_key = this.Credential.SecretId;
            string payload_hash = SignHelper.MD5Encrypt(requestPayload);
            string canonical_headers = $"content-type:{contentType}\nhost:{endpoint}";

           

            // method  canonical_uri canonical_querystring user_key timestamp payload_hash canonical_headers
            string string2sign = $"{httpRequestMethod}\n{canonical_uri}\n{canonical_querystring}\n{user_key}\n{requestTimestamp}\n{payload_hash}\n{canonical_headers}";
            Console.WriteLine($"string2sign:{string2sign}");
            string signature = SignHelper.Sign(Credential.SecretKey, string2sign, Profile.SignMethod);
            Console.WriteLine($"signature:{signature}");
            //'Authorization: hmac-auth-v1# + ACCESS_KEY + # + base64_encode(SIGNATURE) + # + ALGORITHM + # + DATE + # + SIGNED_HEADERS' 

            string authorization = $"hmac-auth-v1#{Credential.SecretId}#{signature}#{Profile.SignMethod}#{requestTimestamp}#{signedHeaders}";
            Console.WriteLine($"authorization:{authorization}");
            Dictionary<string, string> headers = new Dictionary<string, string>();
            headers.Add("Authorization", authorization);
            headers.Add("Host", endpoint);
            headers.Add("Content-Type", contentType);
            headers.Add("X-MT-Timestamp", requestTimestamp);
            headers.Add("X-MT-Version", this.ApiVersion);
 
            if (!string.IsNullOrEmpty(this.Credential.Token))
            {
                headers.Add("X-MT-Token", this.Credential.Token);
            }
             
            return headers;
        } 
 
         

        public long ToTimestamp()
        {
            DateTimeOffset expiresAtOffset = DateTimeOffset.Now;
            var totalSeconds = expiresAtOffset.ToUnixTimeMilliseconds();
            return totalSeconds; 
        }
    }
}
