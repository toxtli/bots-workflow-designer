var test = require("tape");
var mapLimit = require("./");

test("one at a time", function(t) {
	var waiting = false;
	var stream = mapLimit(function(data, callback) {
		t.ok( ! waiting);
		waiting = true;
		setTimeout(function() {
			waiting = false;
			callback(null, data);
		}, 100);
	}, 1);
	stream.write("a");
	stream.write("b");
	stream.write("c");
	stream.end();

	var datas = [];
	stream.on("data", function(data) {
		datas.push(data);
	});
	stream.on("end", function() {
		t.equal(datas.length, 3);
		t.equal(datas[0], "a");
		t.equal(datas[1], "b");
		t.equal(datas[2], "c");
		t.end();
	});
});
