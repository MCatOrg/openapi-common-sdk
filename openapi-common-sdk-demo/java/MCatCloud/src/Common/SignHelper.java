package Common;

import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;
import javax.xml.bind.DatatypeConverter;
import java.io.UnsupportedEncodingException;
import java.math.BigInteger;
import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;
import java.security.InvalidKeyException;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.TreeMap;

public class SignHelper {
    private static final Charset UTF8 = StandardCharsets.UTF_8;


    public static String Sign(String secret_key, String string2sign, String SignatureMethod) throws MCatCloudSDKException {

        Mac mac =null;
        String sig = null;
        try {

            if (SignatureMethod == ClientProfile.SIGN_SHA256)
            {
                mac = Mac.getInstance("HmacSHA256");
            }
            else if (SignatureMethod == ClientProfile.SIGN_SHA512)
            {
                mac = Mac.getInstance("HmacSHA512");
            }
            else if (SignatureMethod == ClientProfile.SIGN_SHA1)
            {
                mac = Mac.getInstance("HmacSHA1");
            }

            byte[] hash;
            SecretKeySpec secretKeySpec = new SecretKeySpec(secret_key.getBytes(UTF8), mac.getAlgorithm());

            mac.init(secretKeySpec);
            hash = mac.doFinal(string2sign.getBytes(UTF8));
            //sig = DatatypeConverter.printBase64Binary(hash);
            sig=  DatatypeConverter.printHexBinary(hash).toLowerCase();
        } catch (Exception e) {
            throw new MCatCloudSDKException(e.getClass().getName() + "-" + e.getMessage());
        }
        return sig;
    }


    public static String MD5Encrypt2(String code) {
        byte[] codeBytes = null;
        try {
            codeBytes = MessageDigest.getInstance("md5").digest(code.getBytes());
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException("没有这个md5算法！");
        }
        StringBuilder md5code = new StringBuilder(new BigInteger(1, codeBytes).toString(16));
        for (int i = 0; i < 32 - md5code.length(); i++) {
            md5code.insert(0, "0");
        }
        return md5code.toString();
    }

    public static String MD5Encrypt(String content)   {
        String str =null;
        try {
            Mac mac = Mac.getInstance("HmacMD5");

            mac.update(content.getBytes());
            byte[] result = mac.doFinal();
              str = new BigInteger(1, result).toString(16);
            System.out.println(str);
        }catch (Exception ex){
            System.out.println(ex.getMessage());
        }

        return  str;
    }

    public static String getMD5Str(String str) {
        byte[] digest = null;
        try {
            MessageDigest md5 = MessageDigest.getInstance("md5");
            digest  = md5.digest(str.getBytes("utf-8"));
        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
        }
        //16是表示转换为16进制数
        String md5Str = new BigInteger(1, digest).toString(16);
        return md5Str;
    }

    public static String makeSignPlainText(
            TreeMap<String, String> requestParams, String reqMethod, String host, String path) {

        String retStr = "";
        retStr += reqMethod;
        retStr += host;
        retStr += path;
        retStr += buildParamStr(requestParams, reqMethod);
        return retStr;
    }

    protected static String buildParamStr(
            TreeMap<String, String> requestParams, String requestMethod) {

        String retStr = "";
        for (String key : requestParams.keySet()) {
            String value = requestParams.get(key).toString();
            if (retStr.length() == 0) {
                retStr += '?';
            } else {
                retStr += '&';
            }
            retStr += key.replace("_", ".") + '=' + value;
        }
        return retStr;
    }

    public static String sha256Hex(String s) throws MCatCloudSDKException {
        MessageDigest md;
        try {
            md = MessageDigest.getInstance("SHA-256");
        } catch (NoSuchAlgorithmException e) {
            throw new MCatCloudSDKException("SHA-256 is not supported." + e.getMessage());
        }
        byte[] d = md.digest(s.getBytes(UTF8));
        return DatatypeConverter.printHexBinary(d).toLowerCase();
    }

    public static String sha256Hex(byte[] b) throws MCatCloudSDKException {
        MessageDigest md;
        try {
            md = MessageDigest.getInstance("SHA-256");
        } catch (NoSuchAlgorithmException e) {
            throw new MCatCloudSDKException("SHA-256 is not supported." + e.getMessage());
        }
        byte[] d = md.digest(b);
        return DatatypeConverter.printHexBinary(d).toLowerCase();
    }

    public static byte[] hmac256(byte[] key, String msg) throws MCatCloudSDKException {
        Mac mac;
        try {
            mac = Mac.getInstance("HmacSHA256");
        } catch (NoSuchAlgorithmException e) {
            throw new MCatCloudSDKException("HmacSHA256 is not supported." + e.getMessage());
        }
        SecretKeySpec secretKeySpec = new SecretKeySpec(key, mac.getAlgorithm());
        try {
            mac.init(secretKeySpec);
        } catch (InvalidKeyException e) {
            throw new MCatCloudSDKException(e.getClass().getName() + "-" + e.getMessage());
        }
        return mac.doFinal(msg.getBytes(UTF8));
    }
}
