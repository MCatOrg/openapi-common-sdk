using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MCatCloud.Common
{
    /// <summary>
    /// Client profiles.
    /// </summary>
    public class ClientProfile
    {
        /// <summary>
        /// Constructor.
        /// </summary>
        /// <param name="signMethod">Signature process method.</param>
        /// <param name="httpProfile">HttpProfile instance.</param>
        public ClientProfile(string signMethod, HttpProfile httpProfile)
        {
            this.SignMethod = signMethod;
            this.HttpProfile = httpProfile;
            this.Language = Language.DEFAULT;
        }

        public ClientProfile(string signMethod)
            : this(signMethod, new HttpProfile())
        {

        }

        public ClientProfile()
            : this(SIGN_SHA256)
        {
        }

        /// <summary>
        /// HTTP profiles, refer to <seealso cref="HttpProfile"/>
        /// </summary>
        public HttpProfile HttpProfile { get; set; }

        /// <summary>
        /// Signature process method.
        /// </summary>
        public string SignMethod { get; set; }

        /// <summary>
        /// valid choices: zh-CN, en-US
        /// </summary>
        public Language Language { get; set; }

        /// <summary>
        /// Signature process version 1, with HmacSHA1.
        /// </summary>
        public const string SIGN_SHA1 = "hmac-sha1";

        /// <summary>
        /// Signature process version 1, with HmacSHA256.
        /// </summary>
        public static string SIGN_SHA256 = "hmac-sha256";

        /// <summary>
        /// Signature process version 1, with HmacSHA512.
        /// </summary>
        public static string SIGN_SHA512 = "hmac-sha512";

   
    }
}
