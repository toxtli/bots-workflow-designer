# map-stream-limit

Like [map-stream](https://npmjs.org/package/map-stream) but with a concurrency
limit.

# Example

```js
var map = require("map-stream-limit");

map(function(data, callback) {
	// Do some async stuff here
	// But limited to 5 at a time
}, 5);
```

# API

## `map(asyncFn, limit)`

Create a map-stream with the given asynchronous function but no more than the
given limit will be running at any given time.

# Installation 

```
npm install map-stream-limit
```
