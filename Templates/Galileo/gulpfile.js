/* eslint-disable linebreak-style */
/* eslint-disable no-undef */
var gulp = require('gulp');
var sass = require('gulp-sass');
var prefix = require('gulp-autoprefixer');
var minify = require('gulp-clean-css');
var rev = require('gulp-rev');
var revCollector = require('gulp-rev-collector');
var concat = require('gulp-concat');
var uglify = require('gulp-uglify');
var del = require('del');

var prefixerOptions = {
    overrideBrowserslist: ['last 2 versions']
};


gulp.task('clean', function () {
    return del(['assets', 'misc', 'templates']);
});


// CSS
gulp.task('css', function () {
    return gulp.src('./src/assets/css/galileo.scss')
        .pipe(sass())
        .pipe(prefix(prefixerOptions))
        .pipe(minify())
        .pipe(rev())
        .pipe(gulp.dest('./assets/'))
        .pipe(rev.manifest())
        .pipe(gulp.dest('./temp/rev/css'));
});

//JS
gulp.task('js', function () {
    return gulp.src(['./src/assets/js/PhotoSwipe.js', './src/assets/js/dplayer.js', './src/assets/js/galileo.js'])
        .pipe(concat('galileo.js'))
        .pipe(uglify())
        .pipe(rev())
        .pipe(gulp.dest('./assets/'))
        .pipe(rev.manifest())
        .pipe(gulp.dest('./temp/rev/js'));
});

gulp.task('md5', function () {
    return gulp.src(['./temp/rev/**/*.json', './src/templates/**/*ml'])
        .pipe(revCollector())
        .pipe(gulp.dest('./templates/'));
});

gulp.task('move', function () {
    gulp.src(['./src/assets/statics/**/*'], {base: './src/assets/statics/'})
        .pipe(gulp.dest('./assets/'))
    return gulp.src(['./src/misc/**/*'], { base: './src/misc/' })
        .pipe(gulp.dest('./misc/'));
});

gulp.task('default', gulp.series('clean', gulp.parallel('css', 'js'), 'md5', 'move'));
