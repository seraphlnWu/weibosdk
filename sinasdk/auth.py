# coding=utf8
import urllib2
import time
from error import WeibopError
from utils import build_parameters
from utils import import_simplejson

def _request_access_token(client_id, client_secret, code, redirect_uri=None):
    ''' 
        return access token as object: 
        {"access_token":"your-access-token","expires_in":12345678}
        expires_in is standard unix-epoch-time
    '''
    if not redirect_uri:
        raise WeiboError("21305: Parameter absent: redirect_uri, OAuth2 request")

    auth_url = 'https://api.weibo.com/oauth2/'
    r = _http_post(
            '%s%s' % (auth_url, 'access_token'),
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            code=code,
            grant_type='authorization_code',
        )

    r.expires_in += int(time.time())
    return r


def _request_refresh_token(client_id, client_secret, refresh_token, redirect_uri=None):
    '''
        get refresh token
    '''
    if not redirect_uri:
        raise WeiboError("21305: Parameter absent: redirect_uri, OAuth2 request")

    auth_url = 'https://api.weibo.com/oauth2/'
    r = _http_post(
        '%s%s' % (auth_url, 'access_token'),
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        refresh_token=refresh_token,
        grant_type='refresh_token',
    )
    r.expires_in += int(time.time())
    return r


def _http_post(url, authorization=None, **kw):                               
    return _http_call(url, authorization, **kw)


def _http_call(url, authorization, **kw):
    '''     
        send an http request and expect to return a json object if no error.
    '''     

    json = import_simplejson()
    body = build_parameters(**kw)
    print body
    req = urllib2.Request(url, data=body)
    req.add_header('Authorization', 'OAuth2 %s' % authorization)

    resp = urllib2.urlopen(req)
    body = resp.read()
    r = json.loads(body, object_hook=_obj_hook)
    if hasattr(r, 'error_code'):
        raise WeiboError(getattr(r, 'error', ''))
    return r



class JsonObject(dict):
    ''' 
    general json object that can bind any fields but also act as a dict.
    '''
    def __getattr__(self, attr):
        return self[attr]
 
    def __setattr__(self, attr, value):
        self[attr] = value


def _obj_hook(pairs):
    '''
    convert json object to python object.
    '''
    o = JsonObject()
    for k, v in pairs.iteritems():
        o[str(k)] = v
    return o
