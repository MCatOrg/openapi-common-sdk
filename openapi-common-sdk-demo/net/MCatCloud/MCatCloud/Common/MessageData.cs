using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MCatCloud.Common
{
    /// <summary>
    /// 返回信息
    /// </summary>
    //[Serializable]
    public class InfoData<T>
    {

        /// <summary>
        /// 状态码
        /// </summary>
        public int Code { get; set; }

        /// <summary>
        /// 返回错误详情code
        /// </summary>
        public int ReqCode { get; set; }

        /// <summary>
        /// 说明
        /// </summary>
        public string Message { get; set; }

        /// <summary>
        /// 数据
        /// </summary>
        public T Data { get; set; }
 

         


    }
}
