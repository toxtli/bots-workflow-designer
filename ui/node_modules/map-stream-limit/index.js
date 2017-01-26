// jshint node:true
"use strict";

var through = require("through"),
	map = require("map-stream");

module.exports = function(asyncFn, limit) {
	var waiting = 0,
		ended = false,
		buffer = [];

	var stream = through(write, function() {
		ended = true;
		maybeEnd();
	});

	var mapStream = map(function(data, callback) {
		waiting += 1;
		return asyncFn(data, function() {
			waiting -= 1;
			callback.apply(this, arguments);
			unbuffer();
			maybeEnd();
		});
	});

	mapStream.on("data", stream.queue.bind(stream));

	return stream;

	function write(data) {
		if (waiting >= limit) {
			buffer.push(data);
		}
		else {
			mapStream.write(data);
		}
	}

	function unbuffer() {
		if (buffer.length && waiting < limit) {
			write(buffer.shift());
		}
	}

	function maybeEnd() {
		if (ended && waiting === 0) {
			stream.queue(null);
		}
	}
};
