package Common;

public class ClientProfile {
    public ClientProfile(String signMethod, HttpProfile httpProfile)
    {
        this.signMethod = signMethod;
        this.httpProfile = httpProfile;
        this.language = Language.DEFAULT;
    }



    /// <summary>
    /// HTTP profiles, refer to <seealso cref="HttpProfile"/>
    /// </summary>
    public HttpProfile httpProfile ;

    /// <summary>
    /// Signature process method.
    /// </summary>
    public String signMethod;

    /// <summary>
    /// valid choices: zh-CN, en-US
    /// </summary>
    public String language;

    /// <summary>
    /// Signature process version 1, with HmacSHA1.
    /// </summary>
    public static final String SIGN_SHA1 = "hmac-sha1";

    /// <summary>
    /// Signature process version 1, with HmacSHA256.
    /// </summary>
    public static final String SIGN_SHA256 = "hmac-sha256";

    /// <summary>
    /// Signature process version 1, with HmacSHA512.
    /// </summary>
    public static final String SIGN_SHA512 = "hmac-sha512";
}
