using System;
using System.Collections.Generic;
using System.Linq;
using System.Security.Cryptography;
using System.Text;
using System.Threading.Tasks;

namespace MCatCloud.Common
{
    /// <summary>
    /// Signature helper class.
    /// </summary>
    public class SignHelper
    {
        ///<summary>Generate signature.</summary>
        ///<param name="signKey">Credential SecretKey.</param>
        ///<param name="secret">Plain text to be signed.</param>
        ///<returns>Signature.</returns>
        public static string Sign(string secret_key, string string2sign, string SignatureMethod)
        {
            string signRet = string.Empty;
            if (SignatureMethod == ClientProfile.SIGN_SHA256)
            {
                using (HMACSHA256 mac = new HMACSHA256(Encoding.UTF8.GetBytes(secret_key)))
                {
                    byte[] hash = mac.ComputeHash(Encoding.UTF8.GetBytes(string2sign));
                    signRet = HexDigest(hash);
                }
            }
            else if (SignatureMethod == ClientProfile.SIGN_SHA512)
            {
                using (HMACSHA512 mac = new HMACSHA512(Encoding.UTF8.GetBytes(secret_key)))
                {
                    byte[] hash = mac.ComputeHash(Encoding.UTF8.GetBytes(string2sign));
                    signRet = HexDigest(hash);
                }
            }
            else if (SignatureMethod == ClientProfile.SIGN_SHA1)
            {
                using (HMACSHA1 mac = new HMACSHA1(Encoding.UTF8.GetBytes(secret_key)))
                {
                    byte[] hash = mac.ComputeHash(Encoding.UTF8.GetBytes(string2sign));
                    signRet = HexDigest(hash);
                }
            }
            return signRet;
        }

        private static string HexDigest(byte[] hash) {

            StringBuilder builder = new StringBuilder();
            for (int i = 0; i < hash.Length; i++)
            {
                builder.Append(hash[i].ToString("X2"));
            }

            return builder.ToString().ToLower(); 
        }

        public static string SHA256Hex(string s)
        {
            using (SHA256 algo = SHA256.Create())
            {
                byte[] hashbytes = algo.ComputeHash(Encoding.UTF8.GetBytes(s));
                StringBuilder builder = new StringBuilder();
                for (int i = 0; i < hashbytes.Length; ++i)
                {
                    builder.Append(hashbytes[i].ToString("x2"));
                }
                return builder.ToString();
            }
        }

        public static byte[] HmacSHA256(byte[] key, byte[] msg)
        {
            using (HMACSHA256 mac = new HMACSHA256(key))
            {
                return mac.ComputeHash(msg);
            }
        }


        /// <summary>
        /// MD5加密 
        /// </summary>
        /// <param name="encryptStr">待加密的字符串</param>
        /// <returns></returns>
        public static string MD5Encrypt(string encryptStr)
        {
            using (MD5 md5Hash = MD5.Create())
            {
                byte[] data = md5Hash.ComputeHash(Encoding.UTF8.GetBytes(encryptStr));
                StringBuilder sBuilder = new StringBuilder();
                for (int i = 0; i < data.Length; i++)
                {
                    sBuilder.Append(data[i].ToString("x2"));
                }

                string result = sBuilder.ToString();
                return result;
            }
        }

        private static string BuildParamStr(SortedDictionary<string, string> requestParams, string requestMethod = "GET")
        {
            string retStr = "";
            foreach (string key in requestParams.Keys)
            {
                retStr += string.Format("{0}={1}&", key, requestParams[key]);
            }
            return retStr.TrimEnd('&');
        }

        public static string MakeSignPlainText(SortedDictionary<string, string> requestParams, string requestMethod, string requestHost, string requestPath)
        {
            string retStr = "";
            retStr += requestMethod;
            retStr += requestHost;
            retStr += requestPath;
            retStr += "?";
            retStr += BuildParamStr(requestParams);
            return retStr;
        }
    }
}
