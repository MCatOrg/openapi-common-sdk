using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MCatCloud.Common
{
    public class MCatCloudSDKException : Exception
    {
        public MCatCloudSDKException(string message)
            : this(message, "")
        {

        }

        public MCatCloudSDKException(string message, string requestId) :
            base(message)
        {
            RequestId = requestId;
        }

        /// <summary>
        /// UUID of a request.
        /// </summary>
        public string RequestId { get; private set; }

        public override string ToString()
        {
            return $"message：{Message} requestId{RequestId}";
        }
    }
}
