var client = {
	connectToServer: function(path) {
		webSocket = new WebSocket(path);	
		client.attachWebSocketHandlers(webSocket);
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
    			private_message_window = client.openPrivateConversationWindow(message['username']);
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
	appendBotMessageToChatTextArea: function(username, message) {
		var text_area= $('#chat_text_area');
    	text_area.html(text_area.html() + "<small><p>"+ username +": "+message+"</p></small>");
    	var height = $('#chat_text_area')[0].scrollHeight;
	    $('#chat_text_area').scrollTop(height);
	},
	appendUserMessageToChatTextArea: function(username, colour_rgb, message) {
		var text_area= $('#chat_text_area');
    	text_area.html(text_area.html() + "<small><p><span style='color: rgb("+ colour_rgb +")'>"+ username +": </span>"+ message +"</p></small>");
    	var height = $('#chat_text_area')[0].scrollHeight;
	    $('#chat_text_area').scrollTop(height); 
	},
	addUsernameToUserList: function(username, colour_rgb) {
		$('#chat_user_table_body').html($('#chat_user_table_body').html()+"<tr id='"+username+"' class='private_conversation' name='UserListUsernames'><td style='color: rgb("+ colour_rgb +")' recipient_username='"+username+"'><i class='icon-user icon-white' /></i> "+username+"</a></td></tr>");
	},
	removeUsernameFromUserList: function(username) {
		$('#'+username).remove();
	},
	clearAllUsernamesFromUserList: function() {
		$('tr[name="UserListUsernames"][id!="MoBot"]').each(function(key, value) {
			client.removeUsernameFromUserList($.trim($(value).text()));
		});
	},
	resizeElementsBasedOnPageHeight: function() {
		windowHeight = $(window).height();
		pixelBuffer = 103;
		$('#chat_text_area').height(windowHeight-pixelBuffer);
		$('#scroll_body').height(windowHeight-pixelBuffer);
	},
	openPrivateConversationWindow: function(recipientUsername) {
		roomNumber = $('#chat_user_room_number').val();
		url = '/private-conversation/'+roomNumber+'/'+recipientUsername+'/';
		return window.open(url,'','width=800,height=340');
	},
	sendMessageToServer: function(text) {
		request = {'type':1, 'text': text};
		webSocket.send(JSON.stringify(request));
	},
}

$(document).ready(function(){
	
	re = new RegExp("standalone-room");
	matches = re.exec(window.location.pathname);
	if (matches !== null) {
		client.resizeElementsBasedOnPageHeight();
	}
    private_message_windows = [];
    if ($('#chat_user_room_number').length > 0) {
    	var modal_options = {backdrop: 'static', keyboard: false};
    	$('#login_register_modal').modal(modal_options)	
    }
    
    $('body').on('keyup','#chat_input', function(event) {
        if(event.keyCode == 13){
        	message = $('#chat_input').val();
    		$('#chat_input').val("")
            client.sendMessageToServer(message);
        }
    });
    
    $('body').on('click','#chat_send_message_button', function(event) {
    	message = $('#chat_input').val();
		$('#chat_input').val("")
        client.sendMessageToServer(message);
    });
    
    $('body').on('click','#reconnect_button', function(event) {
    	event.preventDefault();
    	location.reload();
    });
    
    $('body').on('click', 'tr.private_conversation', function(event) {
    	recipient_username = $(event.target).attr("recipient_username");
    	if (recipient_username === undefined) {
    		return;
    	}
		if (private_message_windows[recipient_username] === undefined) {
			client.openPrivateConversationWindow(recipient_username);
		}
    });
    
    $('body').on('change', '#navigation_room_dropdown', function(event) {
    	if ($(event.target).val() !== '0') {
			$(event.target).parent("form").submit();		
    	}
    });
    var tooltip_options = {delay: { show: 500, hide: 0 }, placement: 'right', html: true, title: 'What is this'}; 
    $('#html_code_tooltip').tooltip(tooltip_options)
    $('#private_room_tooltip').tooltip(tooltip_options)
    $('.carousel').carousel({
    	interval: 5000
    })
    
    setTimeout(function() {
    			$(".timed_alert").alert('close');
	} ,3000);
    
    $('body').on('click', '.delete_administrator_buttons', function(event) {
    	event.preventDefault();
    	$($(event.target).parents("div")[0]).children("div").children("input").attr("checked",true);
    	$(event.target).parents("form").submit();
    });
    
    $('body').on('click', '.activate_room_buttons', function(event) {
    	if ($(event.target).attr("id") == "activate_room_button") {
    		$('#id_is_active').attr("checked",true);
    	} else {
    		$('#id_is_active').attr("checked",false);
    	}
    	$('#general_settings_form').submit();
    });
    
    $.ajaxSetup({
        crossDomain: false,
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type)) {
            	var csrftoken = $.cookie('csrftoken');
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    
    $('body').on('click', '#login_register_button', function(event) {
    	event.preventDefault();
    	if ($('#login_register_username').val() !== "" && $('#login_register_password').val() !== "") {
    		$.post("/accounts/generate-token/", { "username": $('#login_register_username').val(), "password": $('#login_register_password').val()},
    		function(data){
    			data = $.parseJSON(data['authentication_token'])[0];
    			if (data.fields.token_string == "") {
    				$('#login_register_error').show();
    				return;
    			}
    			roomNumber = $('#chat_user_room_number').val();
    			client.connectToServer("ws://localhost:7000/"+roomNumber+'/'+data.fields.token_string);
    			$('#login_register_modal').modal('hide')
		 	}, "json");
    	}
	});
    
    $('body').on('click', '#login_as_a_guest_button', function(event) {
    	event.preventDefault();
    	roomNumber = $('#chat_user_room_number').val();
		client.connectToServer("ws://localhost:7000/"+roomNumber)
		$('#login_register_modal').modal('hide')
    });
});
