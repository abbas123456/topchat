var client = {
	connectToServer: function() {
		if ($('#chat_user_room_number').length > 0) {
			roomNumber = $('#chat_user_room_number').val();
			if ($('#chat_user_username').length > 0 && $('#chat_user_password').length > 0) {
				username = $('#chat_user_username').val();
				password = $('#chat_user_password').val();
				webSocket = new WebSocket("wss://localhost:7000/" + roomNumber + '/' + username + '/' + password);
			} else {
				webSocket = new WebSocket("wss://localhost:7000/" + roomNumber);	
			}
			
			client.attachWebSocketHandlers(webSocket);
		}
	},
	attachWebSocketHandlers: function(webSocket) {
		webSocket.onmessage = client.webSocketOnMessageHandler;
	    webSocket.onclose = client.webSocketOnCloseHandler;
	},
	webSocketOnMessageHandler: function(e) {
		message = $.parseJSON(e.data);
    	if (message['type'] == 1) {
    		client.appendBotMessageToChatTextArea(message['username'], message['message'])
    	} else if (message['type'] == 2) {
    		client.appendUserMessageToChatTextArea(message['username'], message['colour_rgb'], message['message'])
    	} else if (message['type'] == 3) {
    		client.addUsernameToUserList(message['username'], message['colour_rgb'])
    	} else if (message['type'] == 4) {
    		client.removeUsernameFromUserList(message['username'])
    	} else if (message['type'] == 5) {
    		var private_message_client = private_message_windows[message['recipient_username']];
    		private_message_client.appendBotMessageToChatTextArea(message['username'], message['message']);
    	} else if (message['type'] == 6) {
    		var private_message_client = private_message_windows[message['recipient_username']];
    		private_message_client.appendUserMessageToChatTextArea(message['username'], message['colour_rgb'], message['message']);
    	} else if (message['type'] == 7) {
    		if (private_message_windows[message['username']] === undefined) {
    			url = '/private-conversation/'+message['username']+'/';
    			private_message_window = window.open(url,'','width=800,height=350');
    			private_message_window.onload = function () {
    				var private_message_client = private_message_windows[message['username']];
        			private_message_client.appendUserMessageToChatTextArea(message['username'], message['colour_rgb'], message['message']);
    			};
    		} else {
    			var private_message_client = private_message_windows[message['username']];
    			private_message_client.appendUserMessageToChatTextArea(message['username'], message['colour_rgb'], message['message']);
    		}
    	}
	},
	webSocketOnCloseHandler: function(e) {
		$('#disconnected_alert').show();
	},
	sendMessageToServer: function(webSocket) {
		message = $('#chat_input').val();
		$('#chat_input').val("")
		webSocket.send(message);
	},
	appendBotMessageToChatTextArea: function(username, message) {
		var text_area= $('#chat_text_area');
    	text_area.html(text_area.html() + "<small><p>"+ username +": "+message+"</p></small>");
	},
	appendUserMessageToChatTextArea: function(username, colour_rgb, message) {
		var text_area= $('#chat_text_area');
    	text_area.html(text_area.html() + "<small><p style='color: rgb("+ colour_rgb +")'>"+ username +": "+ message +"</p></small>");
	},
	addUsernameToUserList: function(username, colour_rgb) {
		var private_conversation_url = "<a class='private_conversation' href='/private-conversation/"+username+"/'>";
		$('#chat_user_table_body').html($('#chat_user_table_body').html()+"<tr id='"+username+"' name='UserListUsernames'><td style='color: rgb("+ colour_rgb +")'>"+private_conversation_url+"<i class='icon-user icon-white' /></i> "+username+"</a></td></tr>");
	},
	removeUsernameFromUserList: function(username) {
		$('#'+username).remove();
	},
	clearAllUsernamesFromUserList: function() {
		$('tr[name="UserListUsernames"][id!="MoBot"]').each(function(key, value) {
			client.removeUsernameFromUserList($.trim($(value).text()));
		});
	}
}

$(document).ready(function(){
	client.connectToServer();
    private_message_windows = [];
                               
    $('body').on('keyup','#chat_input', function(event) {
        if(event.keyCode == 13){
            client.sendMessageToServer(webSocket);
        }
    });
    
    $('body').on('click','#chat_send_message_button', function(event) {
    	client.sendMessageToServer(webSocket);
    });
    
    $('body').on('click','#reconnect_button', function(event) {
    	event.preventDefault();
    	$('#disconnected_alert').hide();
    	client.connectToServer();
        client.clearAllUsernamesFromUserList();
    });
    
    $('body').on('click', 'a.private_conversation', function(event) {
    	event.preventDefault();
    	url = $(event.target).attr("href");
    	re = new RegExp(".*\/(.*)\/$");
		matches = re.exec(url);
		if (matches == null) {
			return;
		} else {
			recipient_username = matches[1];
			if (private_message_windows[recipient_username] === undefined) {
				window.open(url,'','width=800,height=350');				
			}
		}
    	
    });
    
});
