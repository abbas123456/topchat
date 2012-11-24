var client = {
	sendMessageToServer: function(webSocket, recipient_username) {
		message = '<'+recipient_username+'>'+ $('#chat_input').val();
		$('#chat_input').val("")
		webSocket.send(message);
	},
	appendBotMessageToChatTextArea: function(username, message) {
		var text_area= $('#private_conversation_text_area');
    	text_area.html(text_area.html() + "<small><p>"+ username +": "+message+"</p></small>");
    	var height = $('#private_conversation_text_area')[0].scrollHeight;
	    $('#private_conversation_text_area').scrollTop(height); 
	},
	appendUserMessageToChatTextArea: function(username, colour_rgb, message) {
		var text_area= $('#private_conversation_text_area');
    	text_area.html(text_area.html() + "<small><p style='color: rgb("+ colour_rgb +")'>"+ username +": "+ message +"</p></small>");
    	var height = $('#private_conversation_text_area')[0].scrollHeight;
	    $('#private_conversation_text_area').scrollTop(height); 
	},
	getRecipientUsernameFromUrl: function() {
		re = new RegExp(".*\/(.*)\/$");
		matches = re.exec(window.location.pathname);
		if (matches == null) {
			return undefined;
		} else {
			return matches[1];
		}
	}
}

$(document).ready(function() {
	$(window).bind("beforeunload", function() { 
    	window.opener.private_message_windows[client.getRecipientUsernameFromUrl()] = undefined; 
    });
	
	window.opener.private_message_windows[client.getRecipientUsernameFromUrl()] = client;

	$('body').on('keyup','#chat_input', function(event) {
        if(event.keyCode == 13){
            client.sendMessageToServer(window.opener.webSocket, client.getRecipientUsernameFromUrl());
        }
    });
    
    $('body').on('click','#chat_send_message_button', function(event) {
    	client.sendMessageToServer(window.opener.webSocket, client.getRecipientUsernameFromUrl());
    });
});
