from example.openapi.HttpProfile import HttpProfile


class ClientProfile(object):
    unsignedPayload = False

    def __init__(self, signMethod=None, httpProfile=None, language="zh-CN"):
        """SDK profile.

        :param signMethod: The signature method, valid choice: HmacSHA1, HmacSHA256, MT3-HMAC-SHA256
        :type signMethod: str
        :param httpProfile: The http profile
        :type httpProfile: :class:`HttpProfile`
        :param language: Valid choice: en-US, zh-CN.
        :type language: str
        """
        self.httpProfile = HttpProfile() if httpProfile is None else httpProfile
        self.signMethod = "HmacSHA256" if signMethod is None else signMethod
        valid_language = ["zh-CN", "en-US"]
        if language not in valid_language:
            raise Exception("ClientError", "Language invalid, choices: %s" % valid_language)
        self.language = language