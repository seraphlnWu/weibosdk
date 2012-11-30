# coding=utf8

'''
    licence
'''
class WeibopError(StandardError):
    '''
        raise APIError if got failed message.
    '''
    def __init__(self, reason):
        self.reason = reason
        
    def __str__(self):
        return self.reason.encode('utf8')
