var client = {
	connectToServer: function() {
		regex = new RegExp(".*\/(.*)\/$")
		matches = regex.exec(window.location.pathname)
		roomNumber = 1;
		if (matches !== null) {
			roomNumber = matches[1]
		}
		return new WebSocket("wss://localhost:7000/" + roomNumber);
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
	webSocket = client.connectToServer();
    client.attachWebSocketHandlers(webSocket);
    
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
    	webSocket = client.connectToServer();
        client.attachWebSocketHandlers(webSocket);
        client.clearAllUsernamesFromUserList();
    });
    
});
