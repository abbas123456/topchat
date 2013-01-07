var client = {
	sendMessageToServer: function(webSocket, recipient_username, text) {
		if (text !== "") {
			request = {'type':2, 'recipient_username': recipient_username, 'text': text};
			webSocket.send(JSON.stringify(request));
		}
	},
	appendBotMessageToChatTextArea: function(username, message) {
		var text_area= $('#private_conversation_text_area');
    	text_area.html(text_area.html() + "<small><p>"+message+"</p></small>");
    	var height = $('#private_conversation_text_area')[0].scrollHeight;
	    $('#private_conversation_text_area').scrollTop(height); 
	},
	appendUserMessageToChatTextArea: function(username, colour_rgb, message) {
		var text_area= $('#private_conversation_text_area');
		text_area.html(text_area.html() + "<small><p class='user_message'><span style='color: rgb("+ colour_rgb +")'>"+ username +": </span> "+ message +"</p></small>");
    	var height = $('#private_conversation_text_area')[0].scrollHeight;
	    $('#private_conversation_text_area').scrollTop(height); 
	    $('.user_message').last().emoticonize({delay:0});
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
	$('#chat_input').focus();
	
	$('body').on('keyup','#chat_input', function(event) {
        if(event.keyCode == 13){
        	message = $('#chat_input').val();
    		$('#chat_input').val("")
        	client.sendMessageToServer(window.opener.webSocket, client.getRecipientUsernameFromUrl(), message);
        }
    });
    
    $('body').on('blur', '#emoticon_popover', function(event) {
    	$('#emoticon_popover').popover('hide');
    	$('#chat_input').focus();
    });
    
    $('#emoticon_popover').popover({placement: 'top', html: true});
    $('#emoticon_popover').emoticonize();
    $('body').on('click', '#emoticon_popover', function(event) {
    	$('.popover-content').emoticonize();
    });
    $('.popover-content').find("span").live('click', function(event) {
    	emoticonText = $(event.target).html() + ' ';
    	$('#chat_input').val($('#chat_input').val()+emoticonText);
    });
});
