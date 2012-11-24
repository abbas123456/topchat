from autobahn.websocket import WebSocketServerFactory, WebSocketProtocol
from objects import BotMessage, UserJoinedMessage, UserLeftMessage

class BroadcastServerFactory(WebSocketServerFactory):

    def __init__(self, url, api_service, debug=False, debugCodePaths=False):
        WebSocketServerFactory.__init__(self, url, debug=debug, debugCodePaths=debugCodePaths)
        self.api_service = api_service 
        self.rooms = {}
        
    def broadcast(self, message, room_number):
        for client in self.rooms[room_number]:
            client.send_direct_message(message)
            
    def join_room(self, client):
        if hasattr(client, 'encrypted_password'):
            if not self.authenticate_user_with_encrypted_password(client.username, client.encrypted_password):
                client.sendClose(code=WebSocketProtocol.CLOSE_STATUS_CODE_NORMAL, reason="Username or password is incorrect")
                
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
            bot_message = BotMessage("Welcome {0}, to change your username temporarily " 
            "type ':CU username', to register or login type ':RL username password'".format(client.username))
            client.send_direct_message(bot_message)
            
            user_joined_message = UserJoinedMessage(client.username, client.colour_rgb)
            self.broadcast(user_joined_message, client.room_number)

    def is_room_number_valid(self, room_number):
        return self.api_service.get_room_by_room_number(room_number) is not None
      
    def create_room(self, room_number):
        self.rooms[room_number] = []
                
    def authenticate_user_with_encrypted_password(self, username, encrypted_password):
        return self.api_service.get_user_by_username_and_encrypted_password(username,
            encrypted_password) is not None
            
    def leave_room(self, client):
        if hasattr(client, 'room_number') and client.room_number in self.rooms:
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
        return (not new_username in usernames) and (not self.does_user_exist(new_username)) 
    
    
    def get_all_usernames(self, room_number):
        client_usernames = [client.username for client in self.rooms[room_number]] 
        client_usernames.append('MoBot')
        return client_usernames
    
    def register_or_login(self, client, username, password):
        if self.does_user_exist(username):
            if self.authenticate_user_with_raw_password(username, password):
                self.change_username(client, username)
            else:
                bot_message = BotMessage("The login credentials were incorrect. Please try again.")
                client.send_direct_message(bot_message)
        else:
            try:
                self.register_new_user(username, password)
                self.change_username(client, username)
            except ValueError:
                bot_message = BotMessage("WE could not register or log you in")
                client.send_direct_message(bot_message)

    def does_user_exist(self, username):
        return self.api_service.get_user_by_username(username) is not None
    
    def authenticate_user_with_raw_password(self, username, password):
        return self.api_service.get_user_by_username_and_raw_password(username, password) is not None
            
    def register_new_user(self, username, password):
        self.api_service.register_user(username, password)
