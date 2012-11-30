# coding=utf8

import os
import mimetypes

from binder import bind_api
from error import WeibopError
from parser import ModelParser


class API(object):
    """Twitter API"""

    def __init__(
            self,
            access_token,
            app_secret,
            host='api.weibo.com',
            api_root='',
            retry_count=0,
            retry_delay=0,
            retry_errors=None,
            source=None,
            parser=None,
            log=None
        ):
        self.access_token = access_token
        self.client_secret=app_secret
        self.source = source

        self.host = host

        self.api_root = api_root
        self.retry_count = retry_count
        self.retry_delay = retry_delay
        self.retry_errors = retry_errors
        self.parser = parser or ModelParser()
        self.log = log

    """ emotions.json """
    emotions = bind_api(
        path = '/emotions.json',
        payload_type = 'emotion', payload_list = True,
        allowed_param = []
    )

    """ statuses/public_timeline """
    public_timeline = bind_api(
        path = '/statuses/public_timeline.json',
        payload_type = 'status', payload_list = True,
        allowed_param = ['since_id', 'count', 'page'],
    )

    """ statuses/home_timeline """
    home_timeline = bind_api(
        path = '/statuses/home_timeline.json',
        payload_type = 'status', payload_list = True,
        allowed_param = ['since_id', 'max_id', 'count', 'page'],
        require_auth = True,
    )

    """ users/counts """
    users_count = bind_api(
        path = "/users/counts.json", 
        payload_list = True,
        allowed_param = ['access_token', 'source', 'uids'],
        require_auth = True,
    )

    """ statuses/friends_timeline """
    friends_timeline = bind_api(
        path = '/statuses/friends_timeline.json',
        payload_type = 'status', payload_list = True,
        allowed_param = ['since_id', 'max_id', 'count', 'page'],
        require_auth = True
    )
    """ statuses/comment """
    comment = bind_api(
        path = '/comments/create.json',
        method = 'POST',
        payload_type = 'comments',
        allowed_param = ['id', 'comment', 'comment_ori', 'source', 'access_token'],
        require_auth = True
    )
    
    """ statuses/comment_destroy """
    comment_destroy  = bind_api(
        path = '/statuses/comment_destroy/{id}.json',
        method = 'POST',
        payload_type = 'comments',
        allowed_param = ['id'],
        require_auth = True
    )
    
    """ statuses/comments_timeline """
    comments = bind_api(
        path = '/statuses/comments.json',
        payload_type = 'comments', payload_list = True,
        allowed_param = ['id', 'count', 'page'],
        require_auth = True
    )
    
    """ statuses/comments_timeline """
    comments_timeline = bind_api(
        path = '/statuses/comments_timeline.json',
        payload_type = 'comments', payload_list = True,
        allowed_param = ['since_id', 'max_id', 'count', 'page'],
        require_auth = True
    )
    
    """ statuses/comments_by_me """
    comments_by_me = bind_api(
        path = '/comments/by_me.json',
        payload_type = 'comments', payload_list = True,
        allowed_param = ['since_id', 'max_id', 'count', 'page'],
        require_auth = True
    )
    
    """ statuses/comments_to_me """
    comments_to_me = bind_api(
        path = '/comments/to_me.json',
        payload_type = 'comments', payload_list = True,
        allowed_param = ['since_id', 'max_id', 'count', 'page'],
        require_auth = True
    )

    """ statuses/user_timeline """
    user_timeline = bind_api(
        path = '/statuses/user_timeline.json',
        payload_type = 'status', payload_list = True,
        allowed_param = ['id', 'uid', 'screen_name', 'since_id',
                          'max_id', 'count', 'page']
    )

    """ statuses/mentions """
    mentions = bind_api(
        path = '/statuses/mentions.json',
        payload_type = 'status', payload_list = True,
        allowed_param = ['since_id', 'max_id', 'count', 'page'],
        require_auth = True
    )

    """ statuses/counts """
    counts = bind_api(
        path = '/statuses/counts.json',
        payload_type = 'counts', payload_list = True,
        allowed_param = ['ids'],
        require_auth = True
    )
    
    """ statuses/unread """
    unread = bind_api(
        path = '/statuses/unread.json',
        payload_type = 'counts'
    )


    """ statuses/show """
    get_status = bind_api(
        path = '/statuses/show.json',
        payload_type = 'status',
        allowed_param = ['id']
    )

    """ statuses/update """
    update_status = bind_api(
        path = '/statuses/update.json',
        method = 'POST',
        payload_type = 'status',
        allowed_param = ['status', 'lat', 'long', 'source', 'access_token'],
        require_auth = True,
    )
    """ statuses/upload """
    def upload(self, filename, status, lat=None, long=None, source=None):
        if source is None:
            source=self.source
        headers, post_data = API._pack_image(filename, 1024, source=source, status=status, lat=lat, long=long, contentname="pic")
        args = [status]
        allowed_param = ['status']
        
        if lat is not None:
            args.append(lat)
            allowed_param.append('lat')
        
        if long is not None:
            args.append(long)
            allowed_param.append('long')
        
        if source is not None:
            args.append(source)
            allowed_param.append('source')
        return bind_api(
            path = '/statuses/upload.json',            
            method = 'POST',
            payload_type = 'status',
            require_auth = True,
            allowed_param = allowed_param            
        )(self, *args, post_data=post_data, headers=headers)

    """ statuses/upload """
    def upload_result(self, contents, status, contenttype,lat=None, long=None, source=None):
        if source is None:
            source=self.source
        headers, post_data = API._pack_result_image(contents, 1024, source=source, status=status, lat=lat, long=long, contentname="pic", contenttype=contenttype)
        args = [status]
        allowed_param = ['status']

        if lat is not None:
            args.append(lat)
            allowed_param.append('lat')

        if long is not None:
            args.append(long)
            allowed_param.append('long')

        if source is not None:
            args.append(source)
            allowed_param.append('source')

        return bind_api(
            path = '/statuses/upload.json',
            method = 'POST',
            payload_type = 'status',
            require_auth = True,
            allowed_param = allowed_param
        )(self, *args, post_data=post_data, headers=headers)

        
    """ statuses/reply """
    reply = bind_api(
        path = '/comments/reply.json',
        method = 'POST',
        payload_type = 'status',
        allowed_param = ['id', 'cid','comment', 'without_mention'],
        require_auth = True
    )
    
    """ statuses/repost """
    repost = bind_api(
        path = '/statuses/repost.json',
        method = 'POST',
        payload_type = 'status',
        allowed_param = ['id', 'status'],
        require_auth = True
    )

    """ statuses/repost """
    repost_timeline = bind_api(
        path = '/statuses/repost_timeline.json',
        method = 'GET',
        payload_type = 'status',
        payload_list = True,
        allowed_param = ['id', 'since_id', 'max_id', 'count', 'page', 'filter_by_author', 'access_token', 'source'],
    )

    """ comments/show """
    comments_show = bind_api(
        path = '/comments/show.json',
        method = 'GET',
        allowed_param = ['id', 'since_id', 'max_id', 'count', 'page', 'filter_by_author', 'access_token', 'source'],
    )

    """ short_url/share/count """
    short_status = bind_api(
        path = '/short_url/share/counts.json',
        method = "GET",
        allowed_param = ['url_short', 'access_token', 'source'],
    )

    """ short_url/shorten """
    shorten = bind_api(
        path = '/short_url/shorten.json',
        method = 'GET',
        allowed_param = ['url_long', 'access_token', 'source'],
    )

    """ users/counts """
    users_count = bind_api(
        path = '/users/counts.json',
        method = 'GET',
        allowed_param = ['ids', 'access_token', 'source'],
    )
    
    """ statuses/destroy """
    destroy_status = bind_api(
        path = '/statuses/destroy/{id}.json',
        method = 'POST',
        payload_type = 'status',
        allowed_param = ['id'],
        require_auth = True
    )

    """ statuses/repost """
    repost = bind_api(
        path = '/statuses/repost/{id}.json',
        method = 'POST',
        payload_type = 'status',
        allowed_param = ['id'],
        require_auth = True
    )

    """ users/show """
    get_user = bind_api(
        path = '/users/show.json',
        payload_type = 'user',
        allowed_param = ['id', 'user_id', 'screen_name', 'source', 'access_token']
    )
    
    """ Get the authenticated user """
    def me(self):
        return self.get_user(screen_name=self.auth.get_username())

    """ users/search """
    search_users = bind_api(
        path = '/users/search.json',
        payload_type = 'user', payload_list = True,
        require_auth = True,
        allowed_param = ['q', 'per_page', 'page']
    )

    search_status = bind_api(
        path = '/statuses/search.json',
        payload_type = 'user', payload_list = True,
        require_auth = True,
        allowed_param = ['q', 'count', 'page']
    )

    """ statuses/friends """
    friends = bind_api(
        path = '/friendships/friends.json',
        payload_type = 'user', payload_list = True,
        allowed_param = ['uid', 'screen_name', 'page', 'cursor', 'trime_status']
    )

    """ friendships/followers """
    followers = bind_api(
        path = '/friendships/followers.json',
        payload_type = 'user', payload_list = True,
        allowed_param = ['uid', 'screen_name', 'page', 'cursor']
    )

    """ direct_messages """
    direct_messages = bind_api(
        path = '/direct_messages.json',
        payload_type = 'direct_message', payload_list = True,
        allowed_param = ['since_id', 'max_id', 'count', 'page'],
        require_auth = True
    )

    """ direct_messages/sent """
    sent_direct_messages = bind_api(
        path = '/direct_messages/sent.json',
        payload_type = 'direct_message', payload_list = True,
        allowed_param = ['since_id', 'max_id', 'count', 'page'],
        require_auth = True
    )
    """ direct_messages/new """
    new_direct_message = bind_api(
        path = '/direct_messages/new.json',
        method = 'POST',
        payload_type = 'direct_message',
        allowed_param = ['id', 'screen_name', 'user_id', 'text'],
        require_auth = True
    )
    
    """ direct_messages/destroy """
    destroy_direct_message = bind_api(
        path = '/direct_messages/destroy/{id}.json',
        method = 'DELETE',
        payload_type = 'direct_message',
        allowed_param = ['id'],
        require_auth = True
    )

    """ friendships/create """
    create_friendship = bind_api(
        path = '/friendships/create.json',
        method = 'POST',
        payload_type = 'user',
        allowed_param = ['id', 'user_id', 'screen_name', 'follow'],
        require_auth = True
    )

    """ friendships/destroy """
    destroy_friendship = bind_api(
        path = '/friendships/destroy.json',
        method = 'DELETE',
        payload_type = 'user',
        allowed_param = ['id', 'user_id', 'screen_name'],
        require_auth = True
    )

    """ friendships/exists """
    exists_friendship = bind_api(
        path = '/friendships/exists.json',
        payload_type = 'json',
        allowed_param = ['user_a', 'user_b']
    )

    """ friendships/show """
    show_friendship = bind_api(
        path = '/friendships/show.json',
        payload_type = 'friendship',
        allowed_param = ['source_id', 'source_screen_name',
                          'target_id', 'target_screen_name']
    )

    """ statuses/show """
    statuses_show = bind_api(
        path = '/statuses/show.json',
        allowed_param = ['id', 'access_token', 'source'],
    )

    """ friends/ids """
    friends_ids = bind_api(
        path = '/friendships/friends/ids.json',
        payload_type = 'json',
        allowed_param = ['uid', 'screen_name', 'cursor', 'count'],
        require_auth = True
    )

    """ followers/ids """
    followers_ids = bind_api(        
        path = '/friendships/followers/ids.json',
        payload_type = 'json',
        allowed_param = ['uid', 'screen_name', 'cursor', 'count'],
    )

    """ account/verify_credentials """
    def verify_credentials(self):
        try:
            return bind_api(
                path = '/account/verify_credentials.json',
                payload_type = 'user',
                require_auth = True
            )(self)
        except WeibopError:
            return False

    """ account/end_session """
    def end_session(self):
        try:
            return bind_api(
                path = '/account/end_session.json',
                method = 'POST',
                payload_type = 'user',
                require_auth = True
            )(self)
        except WeibopError:
            return False

    """ account/rate_limit_status """
    rate_limit_status = bind_api(
        path = '/account/rate_limit_status.json',
        payload_type = 'json'
    )

    """ account/update_delivery_device """
    set_delivery_device = bind_api(
        path = '/account/update_delivery_device.json',
        method = 'POST',
        allowed_param = ['device'],
        payload_type = 'user',
        require_auth = True
    )

    """ account/update_profile_colors """
    update_profile_colors = bind_api(
        path = '/account/update_profile_colors.json',
        method = 'POST',
        payload_type = 'user',
        allowed_param = ['profile_background_color', 'profile_text_color',
                          'profile_link_color', 'profile_sidebar_fill_color',
                          'profile_sidebar_border_color'],
        require_auth = True
    )
        
    """ account/update_profile_image """
    def update_profile_image(self, filename):
        headers, post_data = API._pack_image(filename=filename, max_size=700, source=self.source)
        return bind_api(
            path = '/account/update_profile_image.json',
            method = 'POST',
            payload_type = 'user',
            require_auth = True
        )(self, post_data=post_data, headers=headers)

    """ account/update_profile_background_image """
    def update_profile_background_image(self, filename, *args, **kargs):
        headers, post_data = API._pack_image(filename, 800)
        bind_api(
            path = '/account/update_profile_background_image.json',
            method = 'POST',
            payload_type = 'user',
            allowed_param = ['tile'],
            require_auth = True
        )(self, post_data=post_data, headers=headers)

    """ account/update_profile """
    update_profile = bind_api(
        path = '/account/update_profile.json',
        method = 'POST',
        payload_type = 'user',
        allowed_param = ['name', 'url', 'location', 'description'],
        require_auth = True
    )

    """ favorites """
    favorites = bind_api(
        path = '/favorites/{id}.json',
        payload_type = 'status', payload_list = True,
        allowed_param = ['id', 'page']
    )

    """ favorites/create """
    create_favorite = bind_api(
        path = '/favorites/create/{id}.json',
        method = 'POST',
        payload_type = 'status',
        allowed_param = ['id'],
        require_auth = True
    )

    """ favorites/destroy """
    destroy_favorite = bind_api(
        path = '/favorites/destroy/{id}.json',
        method = 'DELETE',
        payload_type = 'status',
        allowed_param = ['id'],
        require_auth = True
    )

    """ notifications/follow """
    enable_notifications = bind_api(
        path = '/notifications/follow.json',
        method = 'POST',
        payload_type = 'user',
        allowed_param = ['id', 'user_id', 'screen_name'],
        require_auth = True
    )

    """ notifications/leave """
    disable_notifications = bind_api(
        path = '/notifications/leave.json',
        method = 'POST',
        payload_type = 'user',
        allowed_param = ['id', 'user_id', 'screen_name'],
        require_auth = True
    )

    """ blocks/create """
    create_block = bind_api(
        path = '/blocks/create.json',
        method = 'POST',
        payload_type = 'user',
        allowed_param = ['id', 'user_id', 'screen_name'],
        require_auth = True
    )

    """ blocks/destroy """
    destroy_block = bind_api(
        path = '/blocks/destroy.json',
        method = 'DELETE',
        payload_type = 'user',
        allowed_param = ['id', 'user_id', 'screen_name'],
        require_auth = True
    )

    """ blocks/exists """
    def exists_block(self, *args, **kargs):
        try:
            bind_api(
                path = '/blocks/exists.json',
                allowed_param = ['id', 'user_id', 'screen_name'],
                require_auth = True
            )(self, *args, **kargs)
        except WeibopError:
            return False
        return True

    """ blocks/blocking """
    blocks = bind_api(
        path = '/blocks/blocking.json',
        payload_type = 'user', payload_list = True,
        allowed_param = ['page'],
        require_auth = True
    )

    """ blocks/blocking/ids """
    blocks_ids = bind_api(
        path = '/blocks/blocking/ids.json',
        payload_type = 'json',
        require_auth = True
    )

    """ statuses/repost """
    report_spam = bind_api(
        path = '/report_spam.json',
        method = 'POST',
        payload_type = 'user',
        allowed_param = ['id', 'user_id', 'screen_name'],
        require_auth = True
    )

    """ saved_searches """
    saved_searches = bind_api(
        path = '/saved_searches.json',
        payload_type = 'saved_search', payload_list = True,
        require_auth = True
    )

    """ saved_searches/show """
    get_saved_search = bind_api(
        path = '/saved_searches/show/{id}.json',
        payload_type = 'saved_search',
        allowed_param = ['id'],
        require_auth = True
    )

    """ saved_searches/create """
    create_saved_search = bind_api(
        path = '/saved_searches/create.json',
        method = 'POST',
        payload_type = 'saved_search',
        allowed_param = ['query'],
        require_auth = True
    )

    """ saved_searches/destroy """
    destroy_saved_search = bind_api(
        path = '/saved_searches/destroy/{id}.json',
        method = 'DELETE',
        payload_type = 'saved_search',
        allowed_param = ['id'],
        require_auth = True
    )

    """ help/test """
    def test(self):
        try:
            bind_api(
                path = '/help/test.json',
            )(self)
        except WeibopError:
            return False
        return True

    def create_list(self, *args, **kargs):
        return bind_api(
            path = '/%s/lists.json' % self.auth.get_username(),
            method = 'POST',
            payload_type = 'list',
            allowed_param = ['name', 'mode', 'description'],
            require_auth = True
        )(self, *args, **kargs)

    def destroy_list(self, slug):
        return bind_api(
            path = '/%s/lists/%s.json' % (self.auth.get_username(), slug),
            method = 'DELETE',
            payload_type = 'list',
            require_auth = True
        )(self)

    def update_list(self, slug, *args, **kargs):
        return bind_api(
            path = '/%s/lists/%s.json' % (self.auth.get_username(), slug),
            method = 'POST',
            payload_type = 'list',
            allowed_param = ['name', 'mode', 'description'],
            require_auth = True
        )(self, *args, **kargs)

    lists = bind_api(
        path = '/{user}/lists.json',
        payload_type = 'list', payload_list = True,
        allowed_param = ['user', 'cursor'],
        require_auth = True
    )

    lists_memberships = bind_api(
        path = '/{user}/lists/memberships.json',
        payload_type = 'list', payload_list = True,
        allowed_param = ['user', 'cursor'],
        require_auth = True
    )

    lists_subscriptions = bind_api(
        path = '/{user}/lists/subscriptions.json',
        payload_type = 'list', payload_list = True,
        allowed_param = ['user', 'cursor'],
        require_auth = True
    )

    list_timeline = bind_api(
        path = '/{owner}/lists/{slug}/statuses.json',
        payload_type = 'status', payload_list = True,
        allowed_param = ['owner', 'slug', 'since_id', 'max_id', 'count', 'page']
    )

    get_list = bind_api(
        path = '/{owner}/lists/{slug}.json',
        payload_type = 'list',
        allowed_param = ['owner', 'slug']
    )

    def add_list_member(self, slug, *args, **kargs):
        return bind_api(
            path = '/%s/%s/members.json' % (self.auth.get_username(), slug),
            method = 'POST',
            payload_type = 'list',
            allowed_param = ['id'],
            require_auth = True
        )(self, *args, **kargs)

    def remove_list_member(self, slug, *args, **kargs):
        return bind_api(
            path = '/%s/%s/members.json' % (self.auth.get_username(), slug),
            method = 'DELETE',
            payload_type = 'list',
            allowed_param = ['id'],
            require_auth = True
        )(self, *args, **kargs)

    list_members = bind_api(
        path = '/{owner}/{slug}/members.json',
        payload_type = 'user', payload_list = True,
        allowed_param = ['owner', 'slug', 'cursor']
    )

    def is_list_member(self, owner, slug, user_id):
        try:
            return bind_api(
                path = '/%s/%s/members/%s.json' % (owner, slug, user_id),
                payload_type = 'user'
            )(self)
        except WeibopError:
            return False

    subscribe_list = bind_api(
        path = '/{owner}/{slug}/subscribers.json',
        method = 'POST',
        payload_type = 'list',
        allowed_param = ['owner', 'slug'],
        require_auth = True
    )

    unsubscribe_list = bind_api(
        path = '/{owner}/{slug}/subscribers.json',
        method = 'DELETE',
        payload_type = 'list',
        allowed_param = ['owner', 'slug'],
        require_auth = True
    )

    list_subscribers = bind_api(
        path = '/{owner}/{slug}/subscribers.json',
        payload_type = 'user', payload_list = True,
        allowed_param = ['owner', 'slug', 'cursor']
    )

    def is_subscribed_list(self, owner, slug, user_id):
        try:
            return bind_api(
                path = '/%s/%s/subscribers/%s.json' % (owner, slug, user_id),
                payload_type = 'user'
            )(self)
        except WeibopError:
            return False

    """ trends/available """
    trends_available = bind_api(
        path = '/trends/available.json',
        payload_type = 'json',
        allowed_param = ['lat', 'long']
    )

    """ trends/location """
    trends_location = bind_api(
        path = '/trends/{woeid}.json',
        payload_type = 'json',
        allowed_param = ['woeid']
    )

    """ search """
    search = bind_api(
        search_api = True,
        path = '/search.json',
        payload_type = 'search_result', payload_list = True,
        allowed_param = ['q', 'rpp', 'page', 'callback', 'geocode']
    )
    search.pagination_mode = 'page'

    """ trends """
    trends = bind_api(
        search_api = True,
        path = '/trends.json',
        payload_type = 'json'
    )

    """ trends/current """
    trends_current = bind_api(
        search_api = True,
        path = '/trends/current.json',
        payload_type = 'json',
        allowed_param = ['exclude']
    )

    """ trends/daily """
    trends_daily = bind_api(
        search_api = True,
        path = '/trends/daily.json',
        payload_type = 'json',
        allowed_param = ['date', 'exclude']
    )

    """ trends/weekly """
    trends_weekly = bind_api(
        search_api = True,
        path = '/trends/weekly.json',
        payload_type = 'json',
        allowed_param = ['date', 'exclude']
    )

    """short_url/share/counts"""
    short_url_share_counts = bind_api(
        search_api = True,
        path = '/short_url/share/counts.json',
        payload_type = 'json',
        allowed_param = ['url_short'],
    )

    """trends/statuses"""
    trends_statuses = bind_api(
        path = '/trends/statuses.json', 
        payload_type = 'status', payload_list = True,
        allowed_param = ['trend', 'count', 'page'],
        require_auth = True,
    )

    ''' get_oauth2_token'''
    get_oauth2_token = bind_api(
        path = '/oauth2/get_oauth2_token',
        require_auth = True,
    )

    """ tags """
    tags = bind_api(
        path = '/tags.json',
        payload_type = 'tags',
        payload_list = True,
        allowed_param = ['uid', 'count', 'page', 'access_token', 'source'],
    )

    """ Internal use only """
    @staticmethod
    def _pack_image(filename, max_size, source=None, status=None, lat=None, long=None, contentname="image"):
        """Pack image from file into multipart-formdata post body"""
        # image must be less than 700kb in size
        try:
            if os.path.getsize(filename) > (max_size * 1024):
                raise WeibopError('File is too big, must be less than 700kb.')
        #except os.error, e:
        except os.error:
            raise WeibopError('Unable to access file')

        # image must be gif, jpeg, or png
        file_type = mimetypes.guess_type(filename)
        if file_type is None:
            raise WeibopError('Could not determine file type')
        file_type = file_type[0]
        if file_type not in ['image/gif', 'image/jpeg', 'image/png']:
            raise WeibopError('Invalid file type for image: %s' % file_type)

        # build the mulitpart-formdata body
        fp = open(filename, 'rb')
        BOUNDARY = 'Tw3ePy'
        body = []
        if status is not None:            
            body.append('--' + BOUNDARY)
            body.append('Content-Disposition: form-data; name="status"')
            body.append('Content-Type: text/plain; charset=US-ASCII')
            body.append('Content-Transfer-Encoding: 8bit')
            body.append('')
            body.append(status)
        if source is not None:            
            body.append('--' + BOUNDARY)
            body.append('Content-Disposition: form-data; name="source"')
            body.append('Content-Type: text/plain; charset=US-ASCII')
            body.append('Content-Transfer-Encoding: 8bit')
            body.append('')
            body.append(source)
        if lat is not None:            
            body.append('--' + BOUNDARY)
            body.append('Content-Disposition: form-data; name="lat"')
            body.append('Content-Type: text/plain; charset=US-ASCII')
            body.append('Content-Transfer-Encoding: 8bit')
            body.append('')
            body.append(lat)
        if long is not None:            
            body.append('--' + BOUNDARY)
            body.append('Content-Disposition: form-data; name="long"')
            body.append('Content-Type: text/plain; charset=US-ASCII')
            body.append('Content-Transfer-Encoding: 8bit')
            body.append('')
            body.append(long)
        body.append('--' + BOUNDARY)
        body.append('Content-Disposition: form-data; name="'+ contentname +'"; filename="%s"' % filename)
        body.append('Content-Type: %s' % file_type)
        body.append('Content-Transfer-Encoding: binary')
        body.append('')
        body.append(fp.read())
        body.append('--' + BOUNDARY + '--')
        body.append('')
        fp.close()        
        body.append('--' + BOUNDARY + '--')
        body.append('')
        body = '\r\n'.join(body)
        # build headers
        headers = {
            'Content-Type': 'multipart/form-data; boundary=Tw3ePy',
            'Content-Length': len(body)
        }

        return headers, body

    @staticmethod
    def _pack_result_image(contents, max_size, source=None, status=None, lat=None, long=None, contentname="image",contenttype='image/png'):
        """Pack image from file into multipart-formdata post body"""
        # image must be less than 700kb in size
        if len(contents) > (max_size * 1024):
            raise WeibopError('File is too big, must be less than 700kb.')

        # image must be gif, jpeg, or png
        file_type = contenttype
        if file_type not in ['image/gif', 'image/jpeg', 'image/png', 'image/pjpeg']:
            raise WeibopError('Invalid file type for image: %s' % file_type)

        # build the mulitpart-formdata body
        BOUNDARY = 'Tw3ePy'
        body = []
        if status is not None:
            body.append('--' + BOUNDARY)
            body.append('Content-Disposition: form-data; name="status"')
            body.append('Content-Type: text/plain; charset=US-ASCII')
            body.append('Content-Transfer-Encoding: 8bit')
            body.append('')
            body.append(status)
        if source is not None:
            body.append('--' + BOUNDARY)
            body.append('Content-Disposition: form-data; name="source"')
            body.append('Content-Type: text/plain; charset=US-ASCII')
            body.append('Content-Transfer-Encoding: 8bit')
            body.append('')
            body.append(source)
        if lat is not None:
            body.append('--' + BOUNDARY)
            body.append('Content-Disposition: form-data; name="lat"')
            body.append('Content-Type: text/plain; charset=US-ASCII')
            body.append('Content-Transfer-Encoding: 8bit')
            body.append('')
            body.append(lat)
        if long is not None:
            body.append('--' + BOUNDARY)
            body.append('Content-Disposition: form-data; name="long"')
            body.append('Content-Type: text/plain; charset=US-ASCII')
            body.append('Content-Transfer-Encoding: 8bit')
            body.append('')
            body.append(long)
        body.append('--' + BOUNDARY)
        body.append('Content-Disposition: form-data; name="'+ contentname +'"; filename="%s"' % 'result.png')
        body.append('Content-Type: %s' % file_type)
        body.append('Content-Transfer-Encoding: binary')
        body.append('')
        body.append(contents)
        body.append('--' + BOUNDARY + '--')
        body.append('')
        # fp.close()        
        body.append('--' + BOUNDARY + '--')
        body.append('')
        body = '\r\n'.join(body)
        # build headers
        headers = {
            'Content-Type': 'multipart/form-data; boundary=Tw3ePy',
            'Content-Length': len(body)
        }

        return headers, body

