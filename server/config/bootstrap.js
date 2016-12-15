var config = require('./config');
var app = require('express')();
var server = require('http').Server(app);
var MongoClient = require('mongodb').MongoClient

module.exports = function () {

    process.on('uncaughtException', function(err) {
        console.log(err);
    });

    // production error handler
    // no stacktraces leaked to user
    app.use(function (err, req, res, next) {
        res.status(err.status || 500);
        res.render('error', {
            message: err.message,
            error: {}
        });
    });

    // handle CORS 
    // https://developer.mozilla.org/en-US/docs/Web/HTTP/Access_control_CORS
    app.use(function (req, res, next) {
        res.header('Access-Control-Allow-Origin', '*');
        res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE');
        res.header('Access-Control-Allow-Headers', 'X-Requested-With, Authorization, Cache-Control, Content-Type');
        next();
    })

    MongoClient.connect(process.env['MONGO_URL'], function (err, db) {
        if (err) throw err;
        server.listen(process.env.PORT);
        require('./routes')(app, db);
    });
    

    return app;

};