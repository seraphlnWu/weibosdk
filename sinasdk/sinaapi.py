# coding=utf8

from api import API
from utils import build_parameters
from error import WeibopError
from datetime import datetime, timedelta
from time import time, mktime
from django.utils import simplejson
from auth import _request_access_token
from auth import _request_refresh_token

import sm_log

logger = sm_log.getLogger('weibo_sdk')


from django.conf import settings

HOST_NAME = 'hostname'
SINAAPI_FOLLOWERS_MAX_COUNT = 2000
SINAAPI_FOLLOWERS_ID_MAX_COUNT = 2000
SINAAPI_FOLLOWERS_MAX_PAGE = 10


class TooManyRequests(Exception):

    def __init__(self,reason):
        self.reason = reason.encode('utf-8')

    def __str__(self):
        return self.reason


def check_remain_requests(msg='Too many requests'):
    '''
        decorator to check remain request times.
    '''
    def dec(fn):
        'real decorator'
        def wrapr(*args, **kwargs):
            'calculate remain request tims.'
            api_obj_self = args[0]
            api_obj_self._testResetTime()

            if api_obj_self.request_limit < 1:
                raise TooManyRequests(msg)

            api_obj_self.request_limit -= 1
            return fn(*args, **kwargs)
        return wrapr

    return dec




class SinaAPI(object):
    """
    """    
    REQUEST_LIMIT = 20000
    STATUS_LIMIT = 90
    MESSAGE_LIMIT = 180
    LIMIT_RESET_INTERVAL = timedelta(seconds = 3600)
    
    def __init__(
        self,
        app_key,
        app_secret,
        redirect_uri=None,
        domain='api.weibo.com',
        response_type='code',
        version='2',
    ):
        self.client_id = app_key
        self.client_secret = app_secret
        self.redirect_uri = redirect_uri
        self.domain = domain
        self.response_type = response_type
        self.version = version
        self.access_token = None
        self.expires = 0.0

        self._resetLimit()
        self.limit_reset_time = datetime.now()+self.LIMIT_RESET_INTERVAL


    def set_access_token(self, access_token, expires):
        '''
            set access_token and expires time to this instance
        '''
        self.access_token = access_token
        self.expires = float(expires)
        self.api = API(access_token, self.client_secret)

    def _resetLimit(self):
        self.request_limit = self.REQUEST_LIMIT
        self.status_limit = self.STATUS_LIMIT
        self.message_limit = self.MESSAGE_LIMIT    


    def _testResetTime(self):
        t = datetime.now()
        if t > self.limit_reset_time:
            self.request_limit = self.getRateLimit().remaining_hits
            self.limit_reset_time = t + self.LIMIT_RESET_INTERVAL
    

    def getAtt(self, key):
        try:
            return self.obj.__getattribute__(key)
        except Exception as e:
            print e
            raise
            return ''
        
    def getAttValue(self, obj, key):
        try:
            return obj.__getattribute__(key)
        except Exception as e:
            print e
            raise
            return ''


    def get_authorize_url(self, redirect_uri=None, display='default'):
        '''
            获取授权链接    
        '''
        redirect_uri = redirect_uri or self.redirect_uri

        if not redirect_uri:
            WeibopError('You should give me a redirect uri :P')                
        return '%s%s?%s' % (
            'https://%s/oauth2/' % (self.domain, ),
            'authorize',
            build_parameters(
                client_id=self.client_id,
                response_type='code',
                display=display,
                redirect_uri=redirect_uri,
            ),
        )

    def request_access_token(
        self,
        client_id,
        client_secret,
        code,
        redirect_uri=None,
    ):
        return _request_access_token(
            self.client_id,
            self.client_secret,
            code,
            self.redirect_uri,
        )

    def request_refresh_token(
        self,
        client_id,
        client_secret,
        refresh_token,
        redirect_uri=None,
    ):
        return _request_refresh_token(
            self.client_id,
            self.client_secret,
            refresh_token,
            self.redirect_uri,
        )

    @check_remain_requests('Too many requests in getCurrentUser')
    def getCurrentUser(self):
        """返回当前登录用户的信息，如果未登录，返回False"""
        logger.info('api-nail')
        try:
            status = self.api.verify_credentials()
        except WeibopError:
            logger.info("WeibopError") 
            return False
        return status

    @check_remain_requests('Too many requests in getTags')
    def getTags(self, uid, count=20, page=None):
        logger.info('api-nail')
        if count > 200:
            raise Exception('Too many tag counts per page.')
        if page:        
            return self.api.tags(uid=uid, count=count, page=page)
        else:
            return self.api.tags(uid=uid, count=count)


    def getDirectMsgs(self, since_id=None, count=200):
        logger.info('api-nail')
        page = 1
        rvl=[]
        while True:
            self._testResetTime()

            if self.request_limit < 1:
                raise TooManyRequests('Too many requests in getDirectMsgs')
            self.request_limit -= 1
            if since_id:
                directMsgs = self.api.direct_messages(since_id=since_id, count=count, page=page)
            else:
                directMsgs = self.api.direct_messages(count=count, page=page)
            rvl.extend(directMsgs)
            if len(directMsgs) < count:
                break;
            page +=1
        return rvl


    def getSentDirectMsgs(self, since_id=None, count=200):
        logger.info('api-nail')
        page = 1
        rvl=[]
        while True:
            self._testResetTime()

            if self.request_limit < 1:
                raise TooManyRequests('Too many requests in getDirectMsgs')
            self.request_limit -= 1
            if since_id:
                directMsgs = self.api.sent_direct_messages(since_id=since_id, count=count, page=page)
            else:
                directMsgs = self.api.sent_direct_messages(count=count, page=page)
            rvl.extend(directMsgs)
            if len(directMsgs) < count:
                break;
            page +=1
        return rvl


    def getFollowers(self, uid, cursor=-1, count=200):
        status = []
        logger.info('api-nail')

        self._testResetTime()

        if self.request_limit < 1:
            raise TooManyRequests('Too many requests in getFollowers')
        self.request_limit -= 1

        try:
            for i in range(3):
                status = self.api.followers(uid=uid, cursor=cursor,count=count)
                if status:
                    break
                else:
                    status = self.api.followers(uid=uid, cursor=cursor,count=count)
        except WeibopError:
            logger.info("WeibopError") 
            return status 

        return status 

    def getFollowersById(self, user_id, cursor=-1, count=200):
        logger.info('api-nail')
        status = []

        i = 0
        try:
            status = self.api.followers(uid=user_id, cursor=cursor, count=count)
            while not status and i < 3:
                status = self.api.followers(uid=user_id, cursor=cursor, count=count)
                i += 1
        except WeibopError:
            logger.info("WeibopError") 
            return status

        return status 

    def getFollowersIds(self, uid):
        logger.info('api-nail')
        cursor = 0
        count = SINAAPI_FOLLOWERS_ID_MAX_COUNT
        rvl=[]
        while True:
            self._testResetTime()
            if self.request_limit < 1:
                raise TooManyRequests('Too many requests in getFollowersIds')
            self.request_limit -= 1
            try:
                status = self.api.followers_ids(uid=uid, cursor=cursor,count=count)
            except WeibopError:
                logger.info("WeibopError") 
                return list(set(rvl))
            if len(status.ids) == 0:
                break;
            else:
                cursor += len(status.ids)
                rvl.extend(status.ids)
        return list(set(rvl))

    @check_remain_requests('Too many requests in getLimitedFollowersIds')
    def getLimitedFollowersIds(self, cursor=-1, count=20):
        logger.info('api-nail')
        status = self.api.followers_ids(cursor=cursor, count=count)
        return {'ids':status.ids, 'next_cursor':status.next_cursor}


    @check_remain_requests('Too many requests in getLimitedFollowersIds')
    def getFriends(
        self,
        uid=None,
        screen_name=None,
        count=200,
        trim_status=0
    ):
        logger.info('api-nail')
        cursor = -1
        rvl=[]
        for i in range(0,SINAAPI_FOLLOWERS_MAX_PAGE):        
            self._testResetTime()
            if self.request_limit < 1:
                logger.info("TooManyRequests") 
                #raise TooManyRequests('Too many requests in getFriends')
                return rvl
            self.request_limit -= 1
            try:
                status = self.api.friends(
                    uid=uid,
                    cursor=cursor,
                    count=count,
                    trim_status=trim_status,
                )
            except WeibopError:
                logger.info("WeibopError") 
                return rvl
            if len(status) == 0:
                break;
            else:
                cursor += len(status)
                rvl.extend(status)
        return rvl

    def getFriendsIds(self, uid=None, screen_name=None, count=200):
        logger.info('api-nail')
        cursor = 0
        rvl=[]
        while True:
            self._testResetTime()
            if self.request_limit < 1:
                raise TooManyRequests('Too many requests in getFriendsIds')
            self.request_limit -= 1
            try:
                status = self.api.friends_ids(
                    uid=uid,
                    cursor=cursor,
                    count=count,
                )
            except WeibopError:
                logger.info("WeibopError") 
                return rvl
            if len(status.ids) == 0:
                break;
            else:
                cursor += len(status.ids)
                rvl.extend(status.ids)
        return rvl

    
    @check_remain_requests('Too many requests in getUserTimeline')
    def getUserTimeline(self, uid=None, since_id=None, count=200, page=1):
        logger.info('api-nail')
        if uid is None and since_id is None:
            return self.api.user_timeline(count=count, page=page)
        else:
            return self.api.user_timeline(uid=uid, since_id=since_id, count=count, page=page)


    @check_remain_requests('Too many requests in getUserTimeline')
    def getPublicTimeline(self, since_id=None, count=200, page=1):
        logger.info('api-nail')
        return self.api.public_timeline(
            since_id=since_id,
            count=count,
            page=page,
        )


    @check_remain_requests('Too many requests in getUserTimeline')
    def getUsersCount(self, uids):
        logger.info('api-nail')
        return self.api.users_count(uids=uids)


    @check_remain_requests('Too many requests in getUserTimeline')
    def getCounts(self, ids):
        logger.info('api-nail')
        return self.api.counts(ids=ids)

    @check_remain_requests('Too many requests in getRepostTimeline')
    def getRepostTimeline(
        self,
        status_id,
        since_id=None,
        max_id=None,
        count=200,
        page=1,
        filter_by_author=0,
    ):
        logger.info('api-nail')
        return self.api.repost_timeline(
            id=status_id,
            since_id=since_id,
            max_id=max_id,
            count=count,
            page=page,
            filter_by_author=filter_by_author,
        )

    @check_remain_requests('Too many requests in getCommentsToMe')
    def getCommentsToMe(self, since_id, count=200, page=1):
        logger.info('api-nail')
        return self.api.comments_to_me(since_id=since_id, count=count, page=page)

    @check_remain_requests('Too many requests in getCommentsToMe')
    def getCommentsShow(
        self,
        id,
        since_id=None,
        max_id=None,
        count=200,
        page=1,
        filter_by_author=0,
    ):
        logger.info('api-nail')
        if count > 200:
            raise Exception("Too many statuses counts per page.")
        
        return self.api.comments_show(
            id=id,
            since_id=since_id,
            max_id=max_id,
            count=count,
            page=page,
            filter_by_author=filter_by_author,
        )


    @check_remain_requests('Too many requests in getCommentsToMe')
    def getShortStatus(self, url_short):
        '''
            获取短链的微博分享数
        '''
        return self.api.short_status(url_short=url_short)
        

    @check_remain_requests('Too many requests in getCommentsToMe')
    def getShorten(self, url_long):
        '''
            根据长链接获取微博的短链接
        '''
        return self.api.shorten(url_long=url_long)


    @check_remain_requests('Too many requests in getCommentsToMe')
    def getUserCount(self, uids):
        '''
            批量得到用户信息
        '''
        logger.info('api-nail')
        return self.api.users_count(uids=uids)

    @check_remain_requests('Too many requests in getCommentsToMe')
    def getCommentsByMe(self, since_id, count=200, page=1):
        logger.info('api-nail')
        return self.api.comments_by_me(since_id=since_id, count=count, page=page)

    @check_remain_requests('Too many requests in getComments')
    def getUnread(self):
        logger.info('api-nail')
        return self.api.unread()


    @check_remain_requests('Too many requests in getComments')
    def getEmotions(self):
        logger.info('api-nail')
        return self.api.emotions()

    @check_remain_requests('Too many requests in getComments')
    def getComments(self, status_id, count=200, page=1):
        logger.info('api-nail')
        return self.api.comments(status_id, count=count, page=page)

    @check_remain_requests('Too many requests in getComments')
    def getMentions(self, since_id, count=200, page=1):
        logger.info('api-nail')
        return self.api.mentions(since_id=since_id, count=count, page=page)


    @check_remain_requests('Too many requests in getLimitedFriendsIds')
    def getLimitedFriendsIds(self, cursor=-1, count=20):
        logger.info('api-nail')
        status = self.api.friends_ids(cursor=cursor, count=count)
        return {'ids':status.ids, 'next_cursor':status.next_cursor}
    
    @check_remain_requests('Too many requests in getUser')
    def getUser(self,user_id):
        #logger.info('api-nail')
        status = self.api.get_user(uid=user_id)
        return status

    @check_remain_requests('Too many requests in getUser')
    def getUserByName(self, screen_name=None):
        logger.info('api-nail')
        userInfo = self.api.get_user(screen_name=screen_name)
        return userInfo

    @check_remain_requests('Too many requests in sendMessage')
    def sendMessage(self,user_id,message):
        logger.info('api-nail')
        status = self.api.new_direct_message(
                    id=user_id, user_id=user_id, text=message)
        return status
    
    @check_remain_requests('Too many requests in updateStatus')
    def updateStatus(self, message):
        logger.info('api-nail')
        status = self.api.update_status(status=message)
        return status
        
    @check_remain_requests('Too many requests in destroyStatus')
    def destroyStatus(self, mid):
        logger.info('api-nail')
        status = self.api.destroy_status(mid)
        mid = self.getAttValue(status,"id")
        text = self.getAttValue(status,"text")
        return status

    @check_remain_requests('Too many requests in showFriendship')
    def showFriendship(self, src_id, target_id):
        logger.info('api-nail')
        src, target = self.api.show_friendship(source_id=src_id, target_id=target_id)
        return src, target

    @check_remain_requests('Too many requests in ifFollowedBy')
    def ifFollowedBy(self, target_id):
        logger.info('api-nail')
        src, target = self.api.show_friendship(target_id=target_id)
        return src.followed_by
    
    @check_remain_requests('Too many requests in comment')
    def comment(self, comment, mid, cid=None):
        logger.info('api-nail')
        status = self.api.comment(id=mid, comment=comment, comment_ori=0)
        ncid = self.getAttValue(status,"id")
        text = self.getAttValue(status,"text")
        return ncid

    @check_remain_requests('Too many requests in comment')
    def reply(self, comment, sid, cid):
        logger.info('api-nail')
        status = self.api.reply(id=sid,cid=cid,comment=comment, without_mention=True)
        ncid = self.getAttValue(status,"id")
        text = self.getAttValue(status,"text")
        return ncid
        
    @check_remain_requests('Too many requests in commentDestroy')
    def commentDestroy(self, cid):
        status = self.api.comment_destroy(cid)
        ncid = self.getAttValue(status,"id")
        text = self.getAttValue(status,"text")

    @check_remain_requests('Too many requests in uploadResult')
    def uploadResult(self, contents, status,contenttype="image/png"):
        logger.info('api-nail')
        status = self.api.upload_result(contents, status,contenttype=contenttype)
        ncid = self.getAttValue(status, "id")
        text = self.getAttValue(status, "text")
        return status

    @check_remain_requests('Too many requests in upload')
    def upload(self, filename, status):
        logger.info('api-nail')
        status = self.api.upload(filename, status)
        ncid = self.getAttValue(status, "id")
        text = self.getAttValue(status, "text")

    @check_remain_requests('Too many requests in createFriendship')
    def createFriendship(self,user_id):
        logger.info('api-nail')
        user = self.api.create_friendship(user_id=user_id)
        return user

    @check_remain_requests('Too many requests in destoryFriendship')
    def destroyFriendship(self,user_id):
        logger.info('api-nail')
        user = self.api.destroy_friendship(user_id=user_id)
        return user

    def getRateLimit(self):
        logger.info('api-nail')
        return self.api.rate_limit_status()


    @check_remain_requests('Too many requests in destoryFriendship')
    def getTrendsStatus(self, trend, province=0, count=200, page=1):
        status = self.api.trends_statuses(
            trend=trend,
            count=count, 
            page=page
        )
        return status


    @check_remain_requests('Too many requests in destoryFriendship')
    def ShowStatus(self, sid):
        logger.info('api-nail')
        return self.api.statuses_show(id=sid)


    def getSearchStatus(self, q, since_id=-1):
        rst_list = []
        
        for i in range(30):
            try:
                status = self.api.search(q, since_id=since_id)
            except Exception as e:
                return rst_list
            
            rst_list.extend(status)
            since_id = status[-1]

        return rst_list 

    def getSearchUser(self, q, page=1):
        rst_list = []
        for i in range(1, 10):
            try:
                status = self.api.search_user(q, page=i)
            except Exception as e:
                return rst_list
            
            rst_list.extend(status)

        return rst_list 

    def get_short_url_share_counts(
        self,
        url_short,
    ):
        return self.api.short_url_share_counts(url_short=url_short)
