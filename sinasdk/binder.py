# coding=utf8

import httplib
import urllib
import time
import re
from error import WeibopError
from utils import convert_to_utf8_str

re_path_template = re.compile('{\w+}')


def bind_api(**config):

    class APIMethod(object):
        
        path = config['path']
        payload_type = config.get('payload_type', None)
        payload_list = config.get('payload_list', False)
        allowed_param = config.get('allowed_param', [])
        method = config.get('method', 'GET')

        def __init__(self, api, args, kargs):

            self.api = api
            self.host = api.host
            self.post_data = kargs.pop('post_data', None)
            self.retry_count = kargs.pop('retry_count', api.retry_count)
            self.retry_delay = kargs.pop('retry_delay', api.retry_delay)
            self.retry_errors = kargs.pop('retry_errors', api.retry_errors)
            self.headers = kargs.pop('headers', {})
            self.api_root = api.api_root
            
            self.build_parameters(args, kargs)
            
            # build api request path
            self.build_path()

            # set headers
            self.headers['Host'] = self.host

        def build_parameters(self, args, kargs):
            self.parameters = {}
            for idx, arg in enumerate(args):
                try:
                    self.parameters[self.allowed_param[idx]] = convert_to_utf8_str(arg)
                except IndexError:
                    raise WeibopError('Too many parameters supplied!')

            for k, arg in kargs.items():
                if arg is None:
                    continue
                if k in self.parameters:
                    raise WeibopError('Multiple values for parameter %s supplied!' % k)

                self.parameters[k] = convert_to_utf8_str(arg)


        def build_path(self):
            for variable in re_path_template.findall(self.path):
                name = variable.strip('{}')

                if name == 'user' and self.api.auth:
                    value = self.api.auth.get_username()
                else:
                    try:
                        value = urllib.quote(self.parameters[name])
                    except KeyError:
                        raise WeibopError('No parameter value found for path variable: %s' % name)
                    del self.parameters[name]

                self.path = self.path.replace(variable, value)

        def execute(self):
            # Build the request URL
            url = self.api_root + self.path
            if self.api.source is not None:
                self.parameters.setdefault('source',self.api.source)

            if len(self.parameters):
                self.headers.setdefault('Authorization', 'OAuth2 %s' % self.api.access_token)
                if self.method == 'GET':
                    url = '%s?%s' % (url, urllib.urlencode(self.parameters))
                else:
                    self.headers.setdefault("User-Agent", "python")
                    if self.post_data is None:
                        #self.headers.setdefault("Accept","text/html")                        
                        self.headers.setdefault("Content-Type","application/x-www-form-urlencoded")
                        self.post_data = urllib.urlencode(self.parameters)

            sTime = time.time()
            retries_performed = 0
            while retries_performed < self.retry_count + 1:
                # Open connection
                # FIXME: add timeout
                conn = httplib.HTTPSConnection(self.host)

                try:
                    conn.request(
                        self.method,
                        url,
                        headers=self.headers,
                        body=self.post_data,
                    )

                    resp = conn.getresponse()
                except Exception as e:
                    raise WeibopError('Failed to send request: %s' % e + "url=" + str(url) +",self.headers="+ str(self.headers))

                # Exit request loop if non-retry error code
                if self.retry_errors:
                    if resp.status not in self.retry_errors: break
                else:
                    if resp.status == 200:
                        break
                    else:
                        pass

                # Sleep before retrying request again
                time.sleep(self.retry_delay)
                retries_performed += 1

            # If an error was returned, throw an exception
            body = resp.read()
            self.api.last_response = resp
            if self.api.log is not None:
                requestUrl = "URL:https://"+ self.host + url
                eTime = '%.0f' % ((time.time() - sTime) * 1000)
                postData = ""
                if self.post_data is not None:
                    postData = ",post:"+ self.post_data[0:500]
                self.api.log.debug(requestUrl +",time:"+ str(eTime)+ postData+",result:"+ body )
            if resp.status != 200:
                try:
                    json = self.api.parser.parse_error(self, body)
                    error_code =  json['error_code']
                    error =  json['error']
                    error_msg = 'error_code:' + error_code +','+ error
                except Exception:
                    error_msg = "Weibo error response: status code = %s" % resp.status
                raise WeibopError(error_msg)
            
            # Parse the response payload
            result = self.api.parser.parse(self, body)
            conn.close()

            return result

    def _call(api, *args, **kargs):
        method = APIMethod(api, args, kargs)
        return method.execute()


    # Set pagination mode
    if 'cursor' in APIMethod.allowed_param:
        _call.pagination_mode = 'cursor'
    elif 'page' in APIMethod.allowed_param:
        _call.pagination_mode = 'page'

    return _call
