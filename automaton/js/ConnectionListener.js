if (!window.tox) {
	window.tox = {};
}

window.tox.lastResult = '';

tox.requestNotifications = function() {
	var url = 'https://www.linkedin.com/chrome/inbox/activity/notifications/v2?rnd=' + (new Date()).getTime();
	$.get(url, function(data) {
		tox.lastResult = data;
		console.log(data);
	});
};

tox.getNotifications = function() {
	return tox.lastResult;
};

tox.getNotifications();