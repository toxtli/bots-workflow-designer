# [gulp](https://github.com/wearefractal/gulp)-rigger

Rigger is a build time include engine for Javascript, CSS, CoffeeScript and in general any type of text file that you wish to might want to "include" other files into.

## Install

Install with [npm](https://npmjs.org/package/gulp-rigger).

```
npm install --save-dev gulp-rigger
```

## Examples

```js
var gulp = require('gulp');
var rigger = require('gulp-rigger');

gulp.task('default', function () {
	gulp.src('app/*.js')
		.pipe(rigger())
		.pipe(gulp.dest('build/'));
});
```
