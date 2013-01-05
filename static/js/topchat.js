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
    		client.addUsernameToUserList(message['username'], message['is_administrator'], message['is_recipient_administator'], message['colour_rgb'])
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
    	} else if (message['type'] == 8) {
    		client.change_username_display_to_blocked(message['username']);
    	} else if (message['type'] == 9) {
    		client.change_username_display_to_unblocked(message['username']);
    	}
	},
	webSocketOnCloseHandler: function(e) {
		$('#disconnected_alert').show();
		$('li.dropdown[recipient_username]').remove()
	},
	appendBotMessageToChatTextArea: function(username, message) {
		var text_area= $('#chat_text_area');
    	text_area.html(text_area.html() + "<small><p>"+message+"</p></small>");
    	var height = $('#chat_text_area')[0].scrollHeight;
	    $('#chat_text_area').scrollTop(height);
	},
	appendUserMessageToChatTextArea: function(username, colour_rgb, message) {
		var text_area= $('#chat_text_area');
    	text_area.html(text_area.html() + "<small><p class='user_message'><span style='color: rgb("+ colour_rgb +")'>"+ username +": </span> "+ message +"</p></small>");
    	var height = $('#chat_text_area')[0].scrollHeight;
	    $('#chat_text_area').scrollTop(height); 
	    $('.user_message').last().emoticonize({delay:0});
	},
	addUsernameToUserList: function(username, is_administrator, is_recipient_administator, colour_rgb) {
		var icon = is_administrator ? 'icon-eye-open' : 'icon-user';
		var administrator_links = is_recipient_administator ? '<li class="divider"></li><li><a class="chat_controls" name="administrator_kick_buttons" href=""><i class="pre-text icon-exclamation-sign"></i>Kick</a></li><li><a class="chat_controls" name="administrator_ban_buttons" href=""><i class="pre-text icon-warning-sign"></i>Ban</a></li>' : '';
		var dropdown_html = '<li><a href="" class="chat_controls" name="private_conversation_buttons"><i class="pre-text icon-envelope"></i>Private conversation</a></li><li class="divider"></li><li><a class="chat_controls" name="block_buttons" href=""><i class="pre-text icon-ban-circle"></i>Block</a></li>'+administrator_links;
		var user_html = "<li recipient_username='"+username+"' class='dropdown'><a class='dropdown-toggle' data-toggle='dropdown' href='#' style='color: rgb("+colour_rgb+")'><i class='"+icon+" icon-white pre-text'></i>"+username+"</a><ul class='dropdown-menu'>"+dropdown_html+"</ul></li>";
		$(user_html).insertAfter($('#chat_user_list').children("ul").children("li").last());
	},
	removeUsernameFromUserList: function(username) {
		$('li.dropdown[recipient_username="'+username+'"]').remove()
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
		$('#chat_user_list').height(windowHeight-pixelBuffer);
	},
	openPrivateConversationWindow: function(recipientUsername) {
		roomNumber = $('#chat_user_room_number').val();
		url = '/private-conversation/'+roomNumber+'/'+recipientUsername+'/';
		return window.open(url,'','width=800,height=340');
	},
	change_username_display_to_blocked: function(username) {
		control_anchor = $('li.dropdown[recipient_username="'+username+'"]').find("a[name='block_buttons']"); 
		control_anchor.html('<i class="pre-text icon-ban-circle"></i>Unblock');
		control_anchor.attr("name", "unblock_buttons");
		username_anchor = $($('li.dropdown[recipient_username="'+username+'"]').find("a")[0]);
		username_anchor.html('<i class="icon-ban-circle icon-white pre-text"></i>'+username);
	},
	change_username_display_to_unblocked: function(username) {
		control_anchor = $('li.dropdown[recipient_username="'+username+'"]').find("a[name='unblock_buttons']"); 
		control_anchor.html('<i class="pre-text icon-ban-circle"></i>Block');
		control_anchor.attr("name", "block_buttons");
		username_anchor = $($('li.dropdown[recipient_username="'+username+'"]').find("a")[0]);
		username_anchor.html('<i class="icon-user icon-white pre-text"></i>'+username);
	},
	sendMessageToServer: function(text) {
		if (text !== "") {
			request = {'type':1, 'text': text};
			webSocket.send(JSON.stringify(request));	
		}
	},
	sendKickMessageToServer: function(username) {
		request = {'type':3, 'username': username};
		webSocket.send(JSON.stringify(request));
	},
	sendBanMessageToServer: function(username) {
		request = {'type':4, 'username': username};
		webSocket.send(JSON.stringify(request));
	},
	sendBlockMessageToServer: function(username) {
		request = {'type':5, 'username': username};
		webSocket.send(JSON.stringify(request));
	},
	sendUnblockMessageToServer: function(username) {
		request = {'type':6, 'username': username};
		webSocket.send(JSON.stringify(request));
	},
	onLoad: function() {
		
		$.ajaxSetup({
	        crossDomain: false,
	        beforeSend: function(xhr, settings) {
	            if (!/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type)) {
	            	var csrftoken = $.cookie('csrftoken');
	                xhr.setRequestHeader("X-CSRFToken", csrftoken);
	            }
	        }
	    });
		
		if ($('#chat_user_room_number').length > 0) {
	    	$('#login_register_modal').modal({backdrop: 'static', keyboard: false});
	    	private_message_windows = [];
	    }
		
		setTimeout(function() {
	    	$(".timed_alert").alert('close');
		} ,3000);
		
		re = new RegExp("standalone-room");
		matches = re.exec(window.location.pathname);
		if (matches !== null) {
			client.resizeElementsBasedOnPageHeight();
		}
		
		var tooltip_options = {delay: { show: 500, hide: 0 }, placement: 'right', html: true, title: 'What is this'}; 
	    $('#html_code_tooltip').tooltip(tooltip_options)
	    $('#private_room_tooltip').tooltip(tooltip_options)
	    
	    $('.carousel').carousel({
	    	interval: 5000
	    })
		
	    $('#emoticon_popover').popover({placement: 'top', html: true});
	    $('#emoticon_popover').emoticonize();
	}
}

$(document).ready(function(){
	client.onLoad();
	
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
    	$('#disconnected_alert').hide();
    	$('#login_register_modal').modal({backdrop: 'static', keyboard: false});
    });
    
    $('body').on('click', '.chat_controls', function(event) {
    	event.preventDefault();
    	recipient_username = $(event.target).parents("li.dropdown").attr("recipient_username");
    	if (recipient_username === undefined) {
    		return;
    	}
    	buttonName = $(event.target).attr("name"); 
    	if (buttonName == "private_conversation_buttons") {
    		if (private_message_windows[recipient_username] === undefined) {
    			client.openPrivateConversationWindow(recipient_username);
    		}
    	} else if (buttonName == "administrator_kick_buttons") {
    		client.sendKickMessageToServer(recipient_username);    		
    	} else if (buttonName == "administrator_ban_buttons") {
    		client.sendBanMessageToServer(recipient_username);   		
    	} else if (buttonName == "block_buttons") {
    		client.sendBlockMessageToServer(recipient_username);
    	} else if (buttonName == "unblock_buttons") {
    		client.sendUnblockMessageToServer(recipient_username);
    	}
    });
    
    $('body').on('change', '#navigation_room_dropdown', function(event) {
    	if ($(event.target).val() !== '0') {
			$(event.target).parent("form").submit();		
    	}
    });
    
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
    
    $('body').on('click', '#login_register_button', function(event) {
    	event.preventDefault();
    	if ($('#login_register_username').val() !== "" && $('#login_register_password').val() !== "") {
    		roomNumber = $('#chat_user_room_number').val();
    		$.post("/accounts/generate-token/", { "username": $('#login_register_username').val(), "password": $('#login_register_password').val(), 'room_id': roomNumber},
    		function(data){
    			if (data['error_message'] !== undefined) {
    				$('#login_register_error').html(data['error_message']);
    				$('#login_register_error').show();
    				return;
    			}
    			token = $.parseJSON(data['authentication_token'])[0];
    			client.connectToServer("wss://localhost:7000/"+roomNumber+'/'+token.fields.token_string);
    			$('#login_register_modal').modal('hide')
		 	}, "json");
    	}
	});
    
    $('body').on('click', '#login_as_a_guest_button', function(event) {
    	event.preventDefault();
    	roomNumber = $('#chat_user_room_number').val();
		client.connectToServer("wss://localhost:7000/"+roomNumber);
		$('#login_register_modal').modal('hide');
    });
    
    $('body').on('blur', '#emoticon_popover', function(event) {
    	$('#emoticon_popover').popover('hide');
    	$('#chat_input').focus();
    });
    
    $('body').on('click', '#emoticon_popover', function(event) {
    	$('.popover-content').emoticonize();
    });
    
    $('.popover-content').find("span").live('click', function(event) {
    	emoticonText = $(event.target).html() + ' ';
    	$('#chat_input').val($('#chat_input').val()+emoticonText);
    });
});
