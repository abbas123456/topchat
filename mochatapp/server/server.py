import sys
import re

from twisted.internet import reactor
from twisted.python import log
from twisted.web.server import Site
from twisted.web.static import File

from autobahn.websocket import WebSocketServerFactory, \
                               WebSocketServerProtocol, \
                               listenWS
                               
class BroadcastServerProtocol(WebSocketServerProtocol):

    def onOpen(self):
        self.factory.register(self)

    def onMessage(self, msg, binary):
        if not binary:
            match = re.match("CHANGE_USERNAME (.*)", msg)
            if match is not None:
                self.factory.change_username(self, match.groups()[0])
            else:
                self.factory.broadcast("{0}: {1}".format(self.factory.get_username(self), msg))

    def connectionLost(self, reason):
        WebSocketServerProtocol.connectionLost(self, reason)
        self.factory.unregister(self)


class BroadcastServerFactory(WebSocketServerFactory):
    """
    Simple broadcast server broadcasting any message it receives to all
    currently connected clients.
    """

    def __init__(self, url, debug=False, debugCodePaths=False):
       WebSocketServerFactory.__init__(self, url, debug=debug, debugCodePaths=debugCodePaths)
       self.clients = {}

    def change_username(self, client, new_username):
        usernames = [client_usernames['username'] for client_usernames in self.clients.values() ]
        if new_username in usernames:
            prepared_message = self.prepareMessage("MoBot: {0} is already in use, please choose another.".format(new_username))
            client.sendPreparedMessage(prepared_message)
        else:
            old_username = self.clients[client]['username'] 
            self.clients[client]['username'] = new_username
            self.broadcast("MoBot: {0} is now known as {1}".format(old_username, new_username))
            
    def get_username(self, client):
        return self.clients[client]['username']
    
    def register(self, client):
        if not client in self.clients:
            print "registered client " + client.peerstr
            username = "Guest{0}".format(re.search(':(.*)', client.peerstr).groups()[0])
            self.clients[client] = {"username" : username}
            prepared_message = self.prepareMessage("MoBot: Welcome {0}, to change your username type 'CHANGE_USERNAME foo'".format(username))
            client.sendPreparedMessage(prepared_message)

    def unregister(self, client):
        if client in self.clients:
            print "unregistered client " + client.peerstr
            del self.clients[client]

    def broadcast(self, msg):
        print "broadcasting prepared message '%s' .." % msg
        prepared_message = self.prepareMessage(msg)
        for c in self.clients:
            c.sendPreparedMessage(prepared_message)
            print "prepared message sent to " + c.peerstr

if __name__ == '__main__':

    ServerFactory = BroadcastServerFactory
    factory = ServerFactory("ws://localhost:7000")

    factory.protocol = BroadcastServerProtocol
    factory.setProtocolOptions(allowHixie76=True)
    listenWS(factory)

    reactor.run()
