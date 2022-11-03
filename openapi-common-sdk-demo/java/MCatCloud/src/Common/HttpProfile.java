package Common;

public class HttpProfile {
    /// <summary>
    /// HTTPS protocol.
    /// </summary>
    public static final String REQ_HTTPS = "https://";

    /// <summary>
    /// HTTP protocol.
    /// </summary>
    public static final String REQ_HTTP = "http://";

    /// <summary>
    /// HTTP method POST.
    /// </summary>
    public static final String REQ_POST = "POST";

    /** Time unit, 1 minute, equals 60 seconds. */
    public static final int TM_MINUTE = 60;



    /// <summary>
    /// HTTP request method.
    /// </summary>
    private String reqMethod;

    /// <summary>
    /// Service endpoint, or domain name.
    /// </summary>
    private String endpoint;

    /// <summary>
    /// HTTP protocol.
    /// </summary>
    private String protocol ;

    /// <summary>
    /// HTTP request timeout value, in seconds.
    /// </summary>
    private int timeout  ;


    public String getReqMethod() {
        return reqMethod;
    }

    public void setReqMethod(String reqMethod) {
        this.reqMethod = reqMethod;
    }

    public String getEndpoint() {
        return endpoint;
    }

    public void setEndpoint(String endpoint) {
        this.endpoint = endpoint;
    }

    public String getProtocol() {
        return protocol;
    }

    public void setProtocol(String protocol) {
        this.protocol = protocol;
    }

    public int getTimeout() {
        return timeout;
    }

    public void setTimeout(int timeout) {
        this.timeout = timeout;
    }



    public HttpProfile(String endpoint,String protocol) {
        this.reqMethod = HttpProfile.REQ_POST;
        this.endpoint = endpoint;
        this.protocol = protocol;
        this.timeout = HttpProfile.TM_MINUTE;
    }




}
