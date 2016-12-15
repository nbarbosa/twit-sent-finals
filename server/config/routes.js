var config = require('./config');

module.exports = function (app, db) {
	
	// this endpoint generates a new token
    app.get('/tweets', function (req, res) {
        var ts = req.query.ts || Number.MAX_SAFE_INTEGER;
        ts = parseFloat(ts);
        console.log(ts);
        var limit = 10;
        var when = req.query.when || 'before';
        
        var query = {
            $lt: ts
        }
        
        if (when == 'after') {
            query = {
                '$gt': ts
            }
            limit = 1;
        }
        console.log(query);
        
        db.collection('tweets').find({
            'ts_created': query,
            'tweet.retweeted_status': {$exists: false}
            }, 
            {  'tweet.id': true, 
               'ts_created': true, 
               'sentiment': true, 
               '_id': true
            },
            { 'sort': [['ts_created', ((when=='before') ? 'desc': 'asc')]],
              'limit': limit
              
            }).toArray(function (err, result) {
                if (err) throw err
                console.log(result);
                res.json(result);
        });
        
    });

    app.get('/stats', function (req, res) {
        db.collection('tweets').count({'sentiment':'positive'}, function (err, posCount){
            if (err) throw err
            db.collection('tweets').count({'sentiment':'negative'}, function (err, negCount){
             if (err) throw err
                res.json({
                    'positive': posCount,
                    'negative': negCount
                });
            })
        });
    });

    app.get('/', function (req, res) {
        res.end(':)');
    });
};