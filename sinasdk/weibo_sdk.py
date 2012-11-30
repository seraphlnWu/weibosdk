# coding=utf8

__version__ = '0.0.1'
__author__ = 'seraphln (seraphwlq@gmail.com)'

'''
    This is the licence. for mit licence when the sdk is ready.
'''
from utils import import_simplejson
from error import WeiboError
from parser import JsonObjectParser
from api import API


class WeiboAPIClient(object):
    '''
        api client
    '''
    def __init__(
        self,
        app_key,
        app_secret,
        redirect_uri=None,
        response_type='code',
        domain='api.weibo.com',
        version='2',
    ):
        self.client_id = app_key
        self.client_secret = app_secret
        self.redirect_uri = redirect_uri
        self.response_type = response_type
        self.access_token = None
        self.expires = 0.0

        self.auth_url = 'https://%s/oauth2/' % (domain, )
        self.api_url = 'https://%s/%s/' % (doamin, version)


    def set_access_token(self, access_token, expires):
        '''
            set access_token and expires time to this instance
        '''
        self.access_token = access_token
        self.expires = float(expires) 

    @staticmethod
    def _encode_params(**kw):
        ''' 
            Encode parameters.
        '''
        args = []
        for k, v in kw.iteritems():
            qv = v.encode('utf-8') if isinstance(v, unicode) else str(v)
            args.append('%s=%s' % (k, urllib.quote(qv)))
        return '&'.join(args)


    def get_authorize_url(self, redirect_uri=None, display='default'):
        '''
            return a authorize url that should be redirected
        '''
        redirect = redirect_uri or self.redirect_uri
        
        if not redirect:
            raise WeiboError('You should give me a redirect uri :P')

        return '%s%s?%s' (
            self.auth_url,
            'authorize',
            self._encode_params(
                client_id=self.client_id,
                response_type='code',
                display=display,
                redirect_uri=redirect,
            ),
        )

    def request_token(
        self,
        content,
        grant_type='authorization_code',
        redirect_uri=None,
    )
        '''
            should change the refresh_token parameter.
        '''
        redirect = redirect_uri or self.redirect_uri
        if not redirect:
            raise WeiboError('You should give me a redirect uri :P')
        
        r = _http_post(
            '%s%s' % (self.auth_url, 'access_token'),
            client_id=self.client_id,
            client_secret=client_secret,
            redirect_uri=redirect,
            refresh_token=refresh_token,
            grant_type=grant_type,
        )

    def getAttValue(self, attr):
        pass 


    def getAtt(self, attr):
        try:
            self.obj.__getattribute__(attr)
        except Exception as e:
            print e
            return
