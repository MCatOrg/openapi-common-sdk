using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MCatCloud.Common
{
    public class Credential
    {
        /// <summary>
        /// SecretId, can only be obtained from Tencent Cloud Management Console.
        /// </summary>
        public string SecretId { get; set; }

        /// <summary>
        /// SecretKey, can only be obtained from Tencent Cloud Management Console.
        /// </summary>
        public string SecretKey { get; set; }

        /// <summary>
        /// Token
        /// </summary>
        public string Token { get; set; }
    }
}
