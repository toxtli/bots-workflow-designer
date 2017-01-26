'use strict';



/////////////////////////////////////////////////////////////////////////////
// GULP PLUGINS
var gulp = require('gulp'),
    watch = require('gulp-watch'),
    autoprefix = require('gulp-autoprefixer'),
    sass = require('gulp-sass'),
    minifyCss = require('gulp-clean-css'),
    rename = require('gulp-rename'),
    concat = require('gulp-concat'),
    uglify = require('gulp-uglify'),
    rigger = require('gulp-rigger'),
    ignore = require('gulp-ignore'),
    imageop = require('gulp-image-optimization'),
    rimraf = require('rimraf'),
    browserSync = require("browser-sync"),
    reload = browserSync.reload;



/////////////////////////////////////////////////////////////////////////////
// GULP PATHS
var path = {
    src: {
        version_html: 'src/version_html/**/*.*',
        version_angular: 'src/version_angular/**/*.*',
        img: 'src/assets/common/img/**/*.*',
        fonts: 'src/assets/common/fonts/**/*.*',
        css: 'src/assets/common/css/**/*.scss',
        js: 'src/assets/common/js/**/*.*',
        vendors_bower: 'src/assets/vendors/bower/**/*.*',
        vendors_manual: 'src/assets/vendors/manual/**/*.*'
    },
    build: {
        version_html: 'build/version_html/',
        version_angular: 'build/version_angular/',
        img: 'build/assets/common/img/',
        fonts: 'build/assets/common/fonts/',
        css: 'build/assets/common/css',
        cssSource: 'build/assets/common/css/source',
        js: 'build/assets/common/js',
        vendors: 'build/assets/vendors'
    },
    watch: {
        templates: 'src/templates/**/*.html',
        version_html: 'src/version_html/**/*.*',
        version_angular: 'src/version_angular/**/*.*',
        img: 'src/assets/common/img/**/*.*',
        fonts: 'src/assets/common/fonts/**/*.*',
        css: 'src/assets/common/css/**/*.scss',
        js: 'src/assets/common/js/**/*.*',
        vendors: 'src/assets/vendors/**/*.*'
    },
    clean: 'build/'
};



/////////////////////////////////////////////////////////////////////////////
// PRINT ERRORS
function printError(error) {
    console.log(error.toString());
    this.emit('end');
}



/////////////////////////////////////////////////////////////////////////////
// BROWSERSYNC SERVE
var config = {
    server: {
        baseDir: "./build"
    },
    files: ['./build/**/*'],
    tunnel: false,
    host: 'localhost',
    port: 9000,
    logPrefix: "frontend",
    watchTask: true
};

gulp.task('serve', function () {
    setTimeout(function () {
        browserSync(config);
    }, 5000)
});



/////////////////////////////////////////////////////////////////////////////
// VERSION_HTML BUILD
gulp.task('version_html:build', function () {
    return gulp.src(path.src.version_html)
        .pipe(ignore.exclude(['_header.html', '_footer.html', '_top-menu.html', '_left-menu.html']))
        .pipe(rigger())
        .on('error', printError)
        .pipe(gulp.dest(path.build.version_html))
        .pipe(reload({stream: true}));
});



/////////////////////////////////////////////////////////////////////////////
// VERSION_ANGULAR BUILD
gulp.task('version_angular:build', function () {
    return gulp.src(path.src.version_angular)
        .pipe(ignore.exclude(['_header.html', '_footer.html', '_top-menu.html', '_left-menu.html']))
        .pipe(rigger())
        .on('error', printError)
        .pipe(gulp.dest(path.build.version_angular))
        .pipe(reload({stream: true}));
});



/////////////////////////////////////////////////////////////////////////////
// VENDORS BUILD
gulp.task('vendors:bower:build', function() {
    return gulp.src(path.src.vendors_bower)
        .pipe(gulp.dest(path.build.vendors))
});
gulp.task('vendors:manual:build', function() {
    return gulp.src(path.src.vendors_manual)
        .pipe(gulp.dest(path.build.vendors))
});



/////////////////////////////////////////////////////////////////////////////
// JAVASCRIPT BUILD
gulp.task('js:build', function () {
    return gulp.src(path.src.js)
        .pipe(gulp.dest(path.build.js))
        .pipe(reload({stream: true}));
});



/////////////////////////////////////////////////////////////////////////////
// STYLES BUILD
gulp.task('css:build', function () {
    return gulp.src(path.src.css)
        .pipe(sass({outputStyle: 'expanded', indentWidth: 4}))
        .on('error', printError)
        .pipe(autoprefix({
            browsers: ['last 30 versions', '> 1%', 'ie 9'],
            cascade: true
        }))
        .pipe(ignore.exclude('mixins.css'))
        .pipe(gulp.dest(path.build.cssSource))
        .pipe(ignore.exclude('main.css'))
        .pipe(minifyCss())
        .pipe(concat('main.css'))
        .pipe(rename({ extname: '.min.css' }))
        .pipe(gulp.dest(path.build.css))
        .pipe(reload({stream: true}))
});



/////////////////////////////////////////////////////////////////////////////
// IMAGES BUILD
gulp.task('img:build', function (cb) {
    gulp.src(path.src.img)
        .pipe(imageop({
            optimizationLevel: 5,
            progressive: true,
            interlaced: true
        }))
        .on('error', printError)
        .pipe(gulp.dest(path.build.img))
        .on('end', cb)
});



/////////////////////////////////////////////////////////////////////////////
// FONTS BUILD
gulp.task('fonts:build', function() {
    return gulp.src(path.src.fonts)
		.pipe(gulp.dest(path.build.fonts))
});



/////////////////////////////////////////////////////////////////////////////
// BUILD ALL
gulp.task('build', [
    'version_html:build',
    'version_angular:build',
    'fonts:build',
    'img:build',
    'css:build',
    'js:build',
    'vendors:bower:build',
    'vendors:manual:build'
]);


/////////////////////////////////////////////////////////////////////////////
// WATCH ALL
gulp.task('watch', function(){
    watch([path.watch.templates], function(event, cb) {
        gulp.start('version_html:build');
        gulp.start('version_angular:build');
    });
    watch([path.watch.version_html], function(event, cb) {
        gulp.start('version_html:build');
    });
    watch([path.watch.version_angular], function(event, cb) {
        gulp.start('version_angular:build');
    });
    watch([path.watch.img], function(event, cb) {
        gulp.start('img:build');
    });
    watch([path.watch.fonts], function(event, cb) {
        gulp.start('fonts:build');
    });
    watch([path.watch.css], function(event, cb) {
        gulp.start('css:build');
    });
    watch([path.watch.js], function(event, cb) {
        gulp.start('js:build');
    });
    watch([path.watch.vendors], function(event, cb) {
        gulp.start('vendors:bower:build');
        gulp.start('vendors:manual:build');
    });
});



/////////////////////////////////////////////////////////////////////////////
// CLEAN PRODUCTION
gulp.task('clean', function (cb) {
    rimraf(path.clean, cb);
});



/////////////////////////////////////////////////////////////////////////////
// DEFAULT TASK
gulp.task('default', ['build', 'serve', 'watch']);

