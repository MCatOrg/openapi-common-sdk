import copy
from datetime import datetime
import hashlib
import json
import random
import sys
import time
import uuid
import warnings
import logging
import logging.handlers
from urllib.parse import urlencode

import requests
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

from example.openapi.ClientProfile import ClientProfile
from example.openapi.mcat_sdk_exception import MCatSDKException
from example.openapi.request import ApiRequest, RequestInternal
from example.openapi.sign import Sign

warnings.filterwarnings("ignore")

_json_content = 'application/json'
_multipart_content = 'multipart/form-data'
_form_urlencoded_content = 'application/x-www-form-urlencoded'
_octet_stream = "application/octet-stream"


class EmptyHandler(logging.Handler):
    def emit(self, message):
        pass


LOGGER_NAME = "mcat_sdk_common"
logger = logging.getLogger(LOGGER_NAME)
logger.addHandler(EmptyHandler())


class Req:
   def __init__( self, uri="/", header={},method = "POST"):
       self.uri = uri
       self.header = header
       self.method = method

class CommonClient():

    _requestPath = '/'
    _params = {}
    _apiVersion = ''
    _endpoint = ''
    _sdkVersion = 'SDK_PYTHON_%s' % '1.0.0'
    _default_content_type = _form_urlencoded_content
    FMT = '%(asctime)s %(process)d %(filename)s L%(lineno)s %(levelname)s %(message)s'

    def __init__(self, credential, region, profile=None,req_timeout=60):
        self.credential = credential
        self.region = region
        self.req_timeout = req_timeout
        self.profile = ClientProfile() if profile is None else profile
        is_http = True if self.profile.httpProfile.scheme == "http" else False
        # self.host = self.profile.httpProfile.endpoint
        # url = urlparse(self.host)
        self.host = "http://openapi.r.b2co.cn"
        # if not url.hostname:
        #     if is_http:
        #         self.host = "http://" + str(self.host)
        #     else:
        #         self.host  = "https://" +str(self.host)


    def _build_req_inter(self, params, req_inter, options=None):
        options = options or {}
        if self.profile.signMethod in ("hmac-sha512", "hmac-sha256","hmac-sha1"):
            self._build_req_with_signature( params, req_inter, options)
        else:
            raise MCatSDKException("ClientError", "Invalid signature method.")


    def _build_req_with_signature(self, params, req, options=None):

        req.header["Content-Type"] =_json_content
        endpoint = self._get_endpoint()
        timestamp = int(time.time())
        req.header["Host"] = endpoint
        req.header["X-MT-RequestClient"] = self._sdkVersion
        req.header["X-MT-Timestamp"] = str(timestamp)
        req.header["X-MT-Version"] = self._apiVersion

        req.data = json.dumps(params)

        signature = self._get_signature(params, req,  options)

        # 'Authorization: hmac-auth-v1# + ACCESS_KEY + # + base64_encode(SIGNATURE) + # + ALGORITHM + # + DATE + # + SIGNED_HEADERS'

        auth = "hmac-auth-v1#%s#%s#%s#%s#content-type;host" % (
            self.credential.secret_id,signature,self.profile.signMethod,str(timestamp))
        req.header["Authorization"] = auth

    def _get_signature(self, params, req,  options=None):
        options = options or {}
        canonical_uri = req.uri
        canonical_querystring = ""
        payload = req.data

        print("payload",payload)

        # 请求体MD5
        payload_hash = hashlib.md5(payload.encode("utf8")).hexdigest()

        canonical_headers = 'content-type:%s\nhost:%s' % (
            req.header["Content-Type"], req.header["Host"])
        user_key = self.credential.secret_id
        timestamp=req.header["X-MT-Timestamp"]
        string2sign = '%s\n%s\n%s\n%s\n%s\n%s\n%s' % (req.method,
                                                        canonical_uri,
                                                        canonical_querystring,
                                                        user_key,
                                                        timestamp,
                                                        payload_hash,
                                                        canonical_headers
                                                        )

        print("string2sign",string2sign)
        return Sign.sign(self.credential.secret_key, string2sign,self.profile.signMethod)


    def _check_status(self, resp_inter):
        if resp_inter.status != 200:
            raise MCatSDKException("ServerNetworkError", resp_inter.data)

    def _get_service_domain(self):
        return self.profile.httpProfile.rootDomain

    def _get_endpoint(self):
        endpoint = self.profile.httpProfile.endpoint
        if endpoint is None:
            endpoint = self._get_service_domain()
        return endpoint

    def call(self, action, params, options=None, headers=None):

        req = Req(action,headers,self.profile.httpProfile.reqMethod)

        self._build_req_inter(params, req, options)

        try:
            url = self.host + req.uri
            print("请求前", req.__dict__)
            http_resp = requests.request(method=self.profile.httpProfile.reqMethod,
                                         url=url,
                                         data=req.data,
                                         headers=req.header,
                                         timeout=self.req_timeout)
            headers = dict(http_resp.headers)
            resp_inter = ResponseInternal(status=http_resp.status_code,
                                          header=headers,
                                          data=http_resp.text)


            self.request_size = 0
            self.response_size = len(resp_inter.data)
            logger.debug("GetResponse %s" % resp_inter)
            print("请求后", resp_inter)

            self._check_status(resp_inter)
            data = resp_inter.data
            return data

        except Exception as e:
            raise MCatSDKException("ClientNetworkError", str(e))

    def call_json(self, action, params, headers=None, options=None):
        """
        Call api with json object and return with json object.

        :type action: str
        :param action: api name e.g. ``DescribeInstances``
        :type params: dict
        :param params: params with this action
        :type headers: dict
        :param headers: request header, like {"X-MT-TraceId": "ffe0c072-8a5d-4e17-8887-a8a60252abca"}
        :type options: dict
        :param options: request options, like {"SkipSign": False, "IsMultipart": False, "IsOctetStream": False, "BinaryParams": []}
        """
        body = self.call(action, params, options, headers)
        response = json.loads(body)
        print("response",response)
        if response["Code"] == 1:
            return response
        else:
            code = response["Code"]
            message = response["Message"]
            ReqCode = response["ReqCode"]
            raise MCatSDKException(code, message, ReqCode)

    def set_stream_logger(self, stream=None, level=logging.DEBUG, log_format=None):
        """
        Add a stream handler

        :type stream: IO[str]
        :param stream: e.g. ``sys.stdout`` ``sys.stdin`` ``sys.stderr``
        :type level: int
        :param level: Logging level, e.g. ``logging.INFO``
        :type log_format: str
        :param log_format: Log message format
        """
        log = logging.getLogger(LOGGER_NAME)
        log.setLevel(level)
        sh = logging.StreamHandler(stream)
        sh.setLevel(level)
        if log_format is None:
            log_format = self.FMT
        formatter = logging.Formatter(log_format)
        sh.setFormatter(formatter)
        log.addHandler(sh)

    def set_file_logger(self, file_path, level=logging.DEBUG, log_format=None):
        """
        Add a file handler

        :type file_path: str
        :param file_path: path of log file
        :type level: int
        :param level: Logging level, e.g. ``logging.INFO``
        :type log_format: str
        :param log_format: Log message format
        """
        log = logging.getLogger(LOGGER_NAME)
        log.setLevel(level)
        mb = 1024 * 1024
        fh = logging.handlers.RotatingFileHandler(file_path, maxBytes=512*mb, backupCount=10)
        fh.setLevel(level)
        if log_format is None:
            log_format = self.FMT
        formatter = logging.Formatter(log_format)
        fh.setFormatter(formatter)
        log.addHandler(fh)

    def set_default_logger(self):
        """
        Set default log handler
        """
        log = logging.getLogger(LOGGER_NAME)
        log.handlers = []
        logger.addHandler(EmptyHandler())


class RequestInternal(object):
    def __init__(self, host="", method="", uri="", header=None, data=""):
        if header is None:
            header = {}
        self.host = host
        self.method = method
        self.uri = uri
        self.header = header
        self.data = data

    def __str__(self):
        headers = "\n".join("%s: %s" % (k, v) for k, v in self.header.items())
        return ("Host: %s\nMethod: %s\nUri: %s\nHeader: %s\nData: %s\n"
                % (self.host, self.method, self.uri, headers, self.data))


class ResponseInternal(object):
    def __init__(self, status=0, header=None, data=""):
        if header is None:
            header = {}
        self.status = status
        self.header = header
        self.data = data

    def __str__(self):
        headers = "\n".join("%s: %s" % (k, v) for k, v in self.header.items())
        return ("Status: %s\nHeader: %s\nData: %s\n"
                % (self.status, headers, self.data))