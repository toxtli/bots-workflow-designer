if (!window.tox) {
	window.tox = {};
}

window.tox.lastMessage = '';

tox.requestMessages = function() {
	var url = 'https://www.linkedin.com/messaging/conversationsView?includeSent=true&clearUnseen=false&after=' + (new Date()).getTime();
	$.get(url, function(data) {
		tox.lastMessage = data;
		console.log(data);
	});
};

tox.getMessages = function() {
	return tox.lastMessage;
};

tox.getMessages();