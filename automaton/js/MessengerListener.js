if (!window.tox) {
	window.tox = {};
}

window.tox.lastMessage = '';

tox.requestMessages = function() {
	var url = 'https://www.linkedin.com/chrome/inbox/activity/notifications/v2?rnd=' + (new Date()).getTime();
	$.get(url, function(data) {
		tox.lastMessage = data;
		console.log(data);
	});
};

tox.getMessages = function() {
	return tox.lastMessage;
};

tox.getMessages();