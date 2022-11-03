import hashlib
import hmac
import sys
import base64

from example.openapi.mcat_sdk_exception import MCatSDKException


class Sign(object):

    @staticmethod
    def sign(secret_key, sign_str, sign_method):

        print("secret_key: ", secret_key, "sign_str: ", sign_str, "sign_method: ", sign_method)

        sign_str = bytes(sign_str, 'utf-8')
        secret_key = bytes(secret_key, 'utf-8')
        digestmod = None
        if sign_method == 'hmac-sha256':
            digestmod = hashlib.sha256
        elif sign_method == 'hmac-sha512':
            digestmod = hashlib.sha512
        elif sign_method == 'hmac-sha1':
            digestmod = hashlib.sha1
        else:
            raise MCatSDKException("signMethod invalid", "signMethod only support (hmac-sha256, hmac-sha512,hmac-sha1)")

        hashed = hmac.new(secret_key, sign_str, digestmod)

        base_str = base64.b64encode(hashed.digest()).decode("utf-8")

        hash_str = hashed.hexdigest()
        print("hash_str: ", hash_str)

        print("base_str_type: ",type(base_str))

        return hash_str

    @staticmethod
    def sign_tc3(secret_key,  sign_str,sign_method):
        def _hmac_sha256(key, msg):
            return hmac.new(key, msg.encode('utf-8'), hashlib.sha256)

        def _get_signature_key(key):
            # k_date = _hmac_sha256(('TC3' + key).encode('utf-8'), date)
            # k_service  = _hmac_sha256(k_date.digest(), service)
            k_signing = _hmac_sha256(key.encode('utf-8'), 'tc3_request')
            return k_signing.digest()

        signing_key = _get_signature_key(secret_key)
        signature = _hmac_sha256(signing_key, sign_str).hexdigest()
        print("signature",signature)
        return signature


