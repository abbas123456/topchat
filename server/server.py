import sys
import re
import os
import random
import json
import urllib2

from twisted.internet import reactor
from twisted.python import log
from twisted.web.server import Site
from twisted.web.static import File
from autobahn.websocket import WebSocketServerFactory, WebSocketServerProtocol, WebSocketProtocol, listenWS
from objects import BotMessage, UserMessage, UserJoinedMessage, UserLeftMessage, MessageEncoder

class BroadcastServerProtocol(WebSocketServerProtocol):

    def onOpen(self):
        self.username = "Guest{0}".format(re.search(':(.*)', self.peerstr).groups()[0])
        self.colour_rgb = [random.randint(0, 255) for x in range(3)]
        self.room_number = 1 if self.http_request_path[1:] == '' else int(self.http_request_path[1:]) 
        self.factory.register(self)

    def onMessage(self, message_text, binary):
        if not binary:
            match = re.match("CU (.*)", message_text)
            if match is not None:
                new_username = match.groups()[0]
                self.factory.change_username(self, new_username)
            else:
                user_message = UserMessage(self.username, self.colour_rgb, message_text)
                self.factory.broadcast(user_message, self.room_number)

    def connectionLost(self, reason):
        WebSocketServerProtocol.connectionLost(self, reason)
        self.factory.unregister(self)

    def send_direct_message(self, message):
        message_json_string = json.dumps(message, cls=MessageEncoder) 
        BroadcastServerProtocol.sendMessage(self, message_json_string)

class BroadcastServerFactory(WebSocketServerFactory):

    def __init__(self, url, debug=False, debugCodePaths=False):
        WebSocketServerFactory.__init__(self, url, debug=debug, debugCodePaths=debugCodePaths)
        self.rooms = {}
        
    def is_room_number_valid(self, room_number):
        return room_number in [room['id'] for room in json.load(urllib2.urlopen('http://localhost:8080/rooms'))] 
      
    def get_all_usernames(self, room_number):
        client_usernames = [client.username for client in self.rooms[room_number]] 
        client_usernames.append('MoBot')
        return client_usernames
            
    def create_room(self, room_number):
        self.rooms[room_number] = []
                
    def register(self, client):
        if client.room_number not in self.rooms.keys():
            if self.is_room_number_valid(client.room_number):
                self.create_room(client.room_number)
            else:
                client.sendClose(code=WebSocketProtocol.CLOSE_STATUS_CODE_NORMAL, reason="This room does not exist")
                return
            
        room = self.rooms[client.room_number]
            
        if client not in room:
            for current_client in room:
                user_joined_message = UserJoinedMessage(current_client.username, current_client.colour_rgb)
                client.send_direct_message(user_joined_message)
            
            bot_message = BotMessage("{0} has joined the room".format(client.username))
            self.broadcast(bot_message, client.room_number)
            
            room.append(client)
            bot_message = BotMessage("Welcome {0}, to change your username type 'CU foo'".format(client.username))
            client.send_direct_message(bot_message)
            
            user_joined_message = UserJoinedMessage(client.username, client.colour_rgb)
            self.broadcast(user_joined_message, client.room_number)

    def unregister(self, client):
        if client.room_number in self.rooms:
            room = self.rooms[client.room_number]
            if client in room:
                room.remove(client)
                bot_message = BotMessage("{0} has left the room".format(client.username))
                self.broadcast(bot_message, client.room_number)
                user_left_message = UserLeftMessage(client.username)
                self.broadcast(user_left_message, client.room_number)

    def change_username(self, client, new_username):
        if (self.can_username_be_changed(client, new_username)):
            old_username = client.username 
            client.username = new_username
            bot_message = BotMessage("{0} is now known as {1}".format(old_username, new_username))
            self.broadcast(bot_message, client.room_number)
            user_left_message = UserLeftMessage(old_username)
            self.broadcast(user_left_message, client.room_number)
            user_joined_message = UserJoinedMessage(new_username, client.colour_rgb)
            self.broadcast(user_joined_message, client.room_number)
            
        else:
            bot_message = BotMessage("{0} is already in use, please choose another username.".format(new_username))
            client.send_direct_message(bot_message)

    def can_username_be_changed(self, client, new_username):
        usernames = self.get_all_usernames(client.room_number)
        return not new_username in usernames
    
    def broadcast(self, message, room_number):
        for client in self.rooms[room_number]:
            client.send_direct_message(message)
            
    
if __name__ == '__main__':

    ServerFactory = BroadcastServerFactory
    factory = ServerFactory("ws://localhost:7000")

    factory.protocol = BroadcastServerProtocol
    factory.setProtocolOptions(allowHixie76=True)
    listenWS(factory)

    reactor.run()
