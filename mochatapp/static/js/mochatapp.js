var client = {
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
	}
}

$(function() {
	var webSocket = new WebSocket("ws://localhost:7000");
    webSocket.onmessage = function(e) {
    	message = $.parseJSON(e.data);
    	if (message['type'] == 1) {
    		client.appendBotMessageToChatTextArea(message['username'], message['message'])
    	} else if (message['type'] == 2) {
    		client.appendUserMessageToChatTextArea(message['username'], message['colour_rgb'], message['message'])
    	}
    }
    $('body').on('keyup','#chat_input', function(event) {
        if(event.keyCode == 13){
            client.sendMessageToServer(webSocket);
        }
    });
    
    $('body').on('click','#chat_send_message_button', function(event) {
    	client.sendMessageToServer(webSocket);
    });
});
