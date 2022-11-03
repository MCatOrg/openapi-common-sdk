#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import socket
import logging
import requests
import certifi

from example.openapi.mcat_sdk_exception import MCatSDKException

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse



logger = logging.getLogger("tencentcloud_sdk_common")

class ApiRequest(object):
    def __init__(self, host, req_timeout=60, debug=False, proxy=None, is_http=False, certification=None):

        url = urlparse(host)
        if not url.hostname:
            if is_http:
                host = "http://" + host
            else:
                host = "https://" + host
        self.host = host
        self.req_timeout = req_timeout
        self.keep_alive = False
        self.debug = debug
        self.request_size = 0
        self.response_size = 0

    def set_req_timeout(self, req_timeout):
        self.req_timeout = req_timeout

    def is_keep_alive(self):
        return self.keep_alive

    def set_keep_alive(self, flag=True):
        self.keep_alive = flag

    def set_debug(self, debug):
        self.debug = debug

    def _request(self, req_inter):
        print("req_inter:",req_inter)
        req_inter.header["host"] = self.host
        if self.keep_alive:
            req_inter.header["Connection"] = "Keep-Alive"
        if self.debug:
            logger.debug("SendRequest %s" % req_inter)
        if req_inter.method == 'GET':
            req_inter_url = '%s?%s' % (self.host, req_inter.data)
            return requests.request(method=req_inter.method,
                                    url=req_inter_url,
                                    data=None,
                                    headers=req_inter.header,
                                    timeout=self.req_timeout)

        elif req_inter.method == 'POST':
            req_inter_url = '%s%s' % (self.host, req_inter.uri)
            print("req_inter_url: ",req_inter_url)
            return requests.request(method=req_inter.method,
                                    url=req_inter_url,
                                    data=req_inter.data,
                                    headers=req_inter.header,
                                    timeout=self.req_timeout)
        else:
            raise MCatSDKException(
                "ClientParamsError", 'Method only support (GET, POST)')

    def send_request(self, req_inter):
        try:
            http_resp = self._request(req_inter)
            headers = dict(http_resp.headers)
            resp_inter = ResponseInternal(status=http_resp.status_code,
                                          header=headers,
                                          data=http_resp.text)
            self.request_size = 0
            self.response_size = len(resp_inter.data)
            logger.debug("GetResponse %s" % resp_inter)
            return resp_inter
        except Exception as e:
            raise MCatSDKException("ClientNetworkError", str(e))


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
