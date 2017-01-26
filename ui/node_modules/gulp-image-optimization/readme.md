# [gulp](https://github.com/wearefractal/gulp)-image-optimization 

> Minify PNG, JPEG and GIF images with [image-min](https://github.com/kevva/image-min)

*Issues with the output should be reported on the image-min [issue tracker](https://github.com/kevva/image-min/issues).*

## Install

Install with [npm](https://npmjs.org/package/gulp-image-optimization)

```
npm install --save-dev gulp-image-optimization
```


## Example

```
var gulp = require('gulp');
var imageop = require('gulp-image-optimization');

gulp.task('images', function(cb) {
    gulp.src(['src/**/*.png','src/**/*.jpg','src/**/*.gif','src/**/*.jpeg']).pipe(imageop({
        optimizationLevel: 5,
        progressive: true,
        interlaced: true
    })).pipe(gulp.dest('public/images')).on('end', cb).on('error', cb);
});
```

## API

### imageop(options)

See the image-min [options](https://github.com/kevva/image-min#options).


## License

MIT © [Mohamed Rachidi]