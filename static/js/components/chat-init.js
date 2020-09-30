(function() {

    // Slimscroll activation
    $(".chat-contact-list").slimScroll({
        height: "500px",
        color: "rgb(236, 230, 230)",
        disableFadeOut: !0,
        borderRadius: 0,
        size: "0",
        alwaysVisible: !1
    });

    // Slimscroll activation
    $(".message-group").slimScroll({
        height: "300px",
        color: "rgb(236, 230, 230)",
        disableFadeOut: true,
        borderRadius: 0,
        size: "3px",
        alwaysVisible: true
    });

    // Drop chat-pop-window body down
    $('#live-chat header').on('click', function() {
        $('.chat-toggle').slideToggle(300, 'swing');
        $('.chat-message-counter').fadeToggle(300, 'swing');
    });

    // Close chat-pop-window
    $('.close-window').on('click', function(e) {
        e.preventDefault();
        $('#live-chat').fadeOut(300);
    });

    $('#send-message').keypress(function(event){
      var messageText = $('#send-message').val();
    	var keycode = (event.keyCode ? event.keyCode : event.which);
    	if(keycode == '13'){
    		if(messageText.length == 0) {
          alert('Write something!');
        } else {
          alert('Message sent.');
        }
    	}

    });

})();
