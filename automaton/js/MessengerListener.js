if (!window.tox) {
	window.tox = {};
}

// window.tox.lastTimestamp = (((new Date()).getTime() - (8*60*60)) * 1000);
// window.tox.lastTimestamp = 1488120478257;
window.tox.lastMessage = '';

tox.requestMessages = function() {
	var timeVal = ((new Date()).getTime() - (9*1000));
	console.log(timeVal);
	var url = 'https://www.linkedin.com/messaging/conversationsView?includeSent=false&clearUnseen=true&after=' + timeVal;
	$.get(url, function(data) {
		tox.lastMessage = data;
		console.log(data);
	});
};

tox.getMessages = function() {
	return tox.lastMessage;
};

tox.getMessages();