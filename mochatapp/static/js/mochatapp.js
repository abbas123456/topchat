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
		$('#chat_user_table_body').html($('#chat_user_table_body').html()+"<tr id='"+username+"' name='UserListUsernames'><td style='color: rgb("+ colour_rgb +")'><i class='icon-user icon-white' /></i> "+username+"</td></tr>");
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

$(function() {
	client.connectToServer();
    
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
    
});
