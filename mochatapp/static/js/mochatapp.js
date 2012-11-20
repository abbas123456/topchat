var client = {
	appendUserMessageToChatTextArea: function(message) {
		var text_area= $('#chat_text_area');
    	text_area.html(text_area.html() + "<small><p>"+e.data+"</p></small>");
	}
}

$(function() {
	var webSocket = new WebSocket("ws://localhost:7000");
    webSocket.onmessage = function(e) {
    	alert(e.data);
    }
    $('body').on('click','#chat_send_message_button', function(event) {
    	message = $('#chat_input').val();
    	$('#chat_input').val("")
    	webSocket.send(message);
    });
});
