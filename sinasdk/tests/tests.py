# coding=utf8

from sinaapi_factory import *
api = get_api(1720690654)
APP_KEY = "2205141851"
APP_SECRET = "5d1b66b5ea2fd120f02323e10429fabe"

'''
################################################################
路过但是还没有测试通过的api
'''
# test comment
# api.comment(u'就当有', 3516959771827534)
# api.destroyStatus()
# api.comment()
# api.commentDestroy()
# api.createFriendship()
# api.destroyFriendship()
# api.uploadResult()
################################################################


# test getUserByName
# api.getUserByName('seraphln')


# test getMentions
# api.getMentions(since_id=None)

# test getCommentsToMe
# api.getCommentsToMe(since_id=None)

# test getCommentsByMe
# api.getCommentsByMe(since_id=None)

# test getUserTimeline
# api.getUserTimeline(uid=1720690654)

# test getPublicTimeline
# api.getPublicTimeline()

# test getUsersCount
# api.getUsersCount(uids='1720690654')

# test getfollowers
# api.getFollowers(uid=1720690654)

# test getFollowersIds
# api.getFollowersIds(uid=1720690654)

# test getCounts
# api.getCounts(ids='3497835523600269')

# test getFriends
# api.getFriends(uid=1720690654)

# test getFriendsIds
# api.getFriendsIds(uid=1720690654)

# test show friendships
# api.showFriendship(src_id=1720690654, target_id=1720690654)

# test ifFollowBy
# api.ifFollowedBy(target_id=1720690654)

# test ShowStatus
# api.ShowStatus(sid=3497835523600269)

# test getFollowersById
# api.getFollowersById(user_id=1720690654)

# test getTags
# api.getTags(uid=1720690654)

# test getTrendsStatus
# api.getTrendsStatus(u"#image#")

# test getRepostTimeline
# api.getRepostTimeline(status_id=3497835523600269)

# test getCommentsShow
# api.getCommentsShow(id=3497835523600269)

# test getShortStatus
# api.getShortStatus(url_short='http://t.cn/zj5ZYFj')

# test getShorten
# api.getShorten('http://e.weibo.com/1660521332/z7hZN5L95?ref=http%3A%2F%2Fwww.weibomaster.com%2Fhome%2F')

# test getUserCount
# api.getUserCount('1720690654,123456789')

# test updateStatus
# api.updateStatus("This is the status sent by my new weibo sdk")


# test getUser
# api.getUser(1720690654)


# test get authorize url
# print api.get_authorize_url()

# test refresh token
# 2.00EPq8sBDIYO6Cee951ff2111uQgjC
api.request_refresh_token(client_id=APP_KEY, client_secret=APP_SECRET, refresh_token='2.00EPq8sBDIYO6Cee951ff2111uQgjC')
