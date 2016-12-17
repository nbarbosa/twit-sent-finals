var express = require('express');
var session = require('express-session');
var path = require('path');
var logger = require('morgan');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');
var helmet = require('helmet');
var csrf = require('csurf');
var compression = require('compression')

var app = express(); 
app.use(compression())

app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded());
app.use(cookieParser()); 
app.use(session({secret: 'FVG40geQBzMi3AJNSiki'}))

app.use(helmet.crossdomain());
app.use(helmet.csp({
    scriptSrc: ["'self'", "'unsafe-inline'", "'unsafe-eval'", '*.twitter.com', 'twitter.com', '*.twimg.com', 'http://www.google-analytics.com'],
    frameSrc: ["'self'", '*.twitter.com', 'twitter.com', 'periscope.tv', '*.periscope.tv'],
    imgSrc: ["'self'", '*.twitter.com', 'data:', 'http://www.google-analytics.com', 'twitter.com', '*.twimg.com'],
    fontSrc: ["'self' data:", 'https://fonts.googleapis.com', 'http://themes.googleusercontent.com','https://fonts.gstatic.com']
}));

app.use(helmet.xframe());
app.use(helmet.xssFilter());
app.use(helmet.nosniff());
app.use(helmet.ienoopen());
app.use(helmet.nocache());
app.use(helmet.hidePoweredBy());


// production error handler
// no stacktraces leaked to user
app.use(function (err, req, res, next) {
    res.status(err.status || 500);
    res.render('error', {
        message: err.message,
        error: {}
    });
});

// this is annoying
app.use(function(req, res, next){
    if (req.url === '/favicon.ico') {
        res.writeHead(200, {'Content-Type': 'image/x-icon'} );
        res.end();
    } else {
        next();
    }
});

// changes it to use the optimized version for production
app.use(express.static(path.join(__dirname, '/dist')));

app.use(function (req, res, next) {
    res.send(404, 'It seems like what you are looking for is not here.');
});

module.exports = app;
console.log(process.env.PORT);
app.listen(process.env.PORT);