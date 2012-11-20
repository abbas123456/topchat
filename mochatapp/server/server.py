import sys
import re
import random
import json

from twisted.internet import reactor
from twisted.python import log
from twisted.web.server import Site
from twisted.web.static import File

from autobahn.websocket import WebSocketServerFactory, \
                               WebSocketServerProtocol, \
                               listenWS
                               
from objects import BotMessage, UserMessage, UserJoinedMessage, MessageEncoder
                               
class BroadcastServerProtocol(WebSocketServerProtocol):

    def onOpen(self):
        self.username = "Guest{0}".format(re.search(':(.*)', self.peerstr).groups()[0])
        self.colour_rgb = [random.randint(0, 255) for x in range(3)]
        self.factory.register(self)

    def onMessage(self, message_text, binary):
        if not binary:
            match = re.match("CHANGE_USERNAME (.*)", message_text)
            if match is not None:
                new_username = match.groups()[0]
                self.handle_username_change(new_username)
            else:
                user_message = UserMessage(self.username, self.colour_rgb, message_text)
                self.factory.broadcast(user_message)

    def connectionLost(self, reason):
        WebSocketServerProtocol.connectionLost(self, reason)
        self.factory.unregister(self)
        
    def handle_username_change(self, new_username):
        if (self.can_username_be_changed(new_username)):
            old_username = self.username 
            self.username = new_username
            bot_message = BotMessage("{0} is now known as {1}".format(old_username, new_username))
            self.factory.broadcast(bot_message)
        else:
            bot_message = BotMessage("{0} is already in use, please choose another.".format(new_username))
            self.send_direct_message(bot_message)

    def can_username_be_changed(self, new_username):
        usernames = self.factory.get_all_usernames()
        return not new_username in usernames
            
    def send_direct_message(self, message):
        message_json_string = json.dumps(message, cls=MessageEncoder) 
        BroadcastServerProtocol.sendMessage(self, message_json_string)

class BroadcastServerFactory(WebSocketServerFactory):

    def __init__(self, url, debug=False, debugCodePaths=False):
       WebSocketServerFactory.__init__(self, url, debug=debug, debugCodePaths=debugCodePaths)
       self.clients = []

    def get_all_usernames(self):
        return [client.username for client in self.clients]
            
    def register(self, client):
        if not client in self.clients:
            self.clients.append(client)
            bot_message = BotMessage("Welcome {0}, to change your username type 'CHANGE_USERNAME foo'".format(client.username))
            client.send_direct_message(bot_message)

    def unregister(self, client):
        if client in self.clients:
            self.clients.remove(client)

    def broadcast(self, message):
        for client in self.clients:
            client.send_direct_message(message)

    
if __name__ == '__main__':

    ServerFactory = BroadcastServerFactory
    factory = ServerFactory("ws://localhost:7000")

    factory.protocol = BroadcastServerProtocol
    factory.setProtocolOptions(allowHixie76=True)
    listenWS(factory)

    reactor.run()
