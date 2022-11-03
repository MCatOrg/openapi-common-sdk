package Common;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class InfoData<T>
{

    /// <summary>
    /// 状态码
    /// </summary>
    @SerializedName("Code")
    public int Code ;

    /// <summary>
    /// 返回错误详情code
    /// </summary>
    @SerializedName("ReqCode")
    public int ReqCode;

    /// <summary>
    /// 说明
    /// </summary>
    @SerializedName("Message")
    public String Message ;

    /// <summary>
    /// 数据
    /// </summary>
    @SerializedName("Data")
    @Expose
    public T Data ;





}
