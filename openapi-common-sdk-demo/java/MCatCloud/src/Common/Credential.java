package Common;


public class Credential {

    private String secretId;

    private String secretKey;

    private String token;

    public String getSecretId() {
        return secretId;
    }

    public void setSecretId(String secretId) {
        this.secretId = secretId;
    }

    public String getSecretKey() {
        return secretKey;
    }

    public void setSecretKey(String secretKey) {
        this.secretKey = secretKey;
    }

    public String getToken() {
        return token;
    }

    public void setToken(String token) {
        this.token = token;
    }


    public Credential(String secretId, String secretKey) {
        this.secretId = secretId;
        this.secretKey = secretKey;
    }

    public Credential(String secretId, String secretKey, String token) {
        this.secretId = secretId;
        this.secretKey = secretKey;
        this.token = token;
    }
}
