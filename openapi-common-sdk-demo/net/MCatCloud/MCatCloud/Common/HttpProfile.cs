using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MCatCloud.Common
{
    /// <summary>
    /// HTTP profiles.
    /// </summary>
    public class HttpProfile
    {
        /// <summary>
        /// HTTPS protocol.
        /// </summary>
        public static readonly string REQ_HTTPS = "https://";

        /// <summary>
        /// HTTP protocol.
        /// </summary>
        public static readonly string REQ_HTTP = "http://";

        /// <summary>
        /// HTTP method POST.
        /// </summary>
        public static readonly string REQ_POST = "POST";

 

        /// <summary>
        /// Time unit, 60 seconds.
        /// </summary>
        public static readonly int TM_MINUTE = 60;

        public HttpProfile(string endpoint = null, string protocol=null, string reqMethod= "POST", int  reqTimeout= 60)
        {
            this.ReqMethod = reqMethod;
            this.Endpoint = endpoint;
            this.Protocol = protocol?? REQ_HTTPS;
            this.Timeout = reqTimeout;
        }

        /// <summary>
        /// HTTP request method.
        /// </summary>
        public string ReqMethod { get; set; }

        /// <summary>
        /// Service endpoint, or domain name.
        /// </summary>
        public string Endpoint { get; set; }

        /// <summary>
        /// HTTP protocol.
        /// </summary>
        public string Protocol { get; set; }

        /// <summary>
        /// HTTP request timeout value, in seconds.
        /// </summary>
        public int Timeout { get; set; }

        /// <summary>
        /// HTTP proxy settings.
        /// </summary>
        public string WebProxy { get; set; }
    }
}
