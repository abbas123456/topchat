import json
import re

class Message(object):
    
    TYPE_BOT_MESSAGE = 1
    TYPE_USER_MESSAGE = 2
    TYPE_USER_JOINED_MESSAGE = 3
    TYPE_USER_LEFT_MESSAGE = 4
        
    def __init__(self, type, message):
        self.type = type
        self.message = message

class BotMessage(Message):
    def __init__(self, message_text):
        self.username = 'MoBot'
        super(BotMessage, self).__init__(Message.TYPE_BOT_MESSAGE, message_text)
        
class UserMessage(Message):
    def __init__(self, username, colour_rgb, message_text):
        self.username = username
        self.colour_rgb = colour_rgb
        super(UserMessage, self).__init__(Message.TYPE_USER_MESSAGE, self.remove_html_tags(message_text))
    
    def remove_html_tags(self, string):
        regex = re.compile(r'<.*?>')
        return regex.sub('', string)
    
class UserJoinedMessage(Message):
    def __init__(self, username):
        self.username = username
        super(UserJoinedMessage, self).__init__(Message.TYPE_USER_JOINED_MESSAGE, '')

class UserLeftMessage(Message):
    def __init__(self, username):
        self.username = username
        super(UserLeftMessage, self).__init__(Message.TYPE_USER_LEFT_MESSAGE, '')

class MessageEncoder(json.JSONEncoder):
    
    def default(self, object):
        if not isinstance(object, Message):
            return super(MessageEncoder, self).default(object)

        return object.__dict__
