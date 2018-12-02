var express = require('express');
var router = express.Router();
var MongoClient = require('mongodb').MongoClient;
let db;

//Connect as admin to database
MongoClient.connect('mongodb://scancam:camscan1@ds231229.mlab.com:31229/scan-cam-data', (err, client) => {
    if(err){
        console.log(err);
    }
    db = client.db('scan-cam-data');
});
/* GET data listing. */
router.post('/', function(req, res, next) {
    db.collection('data').insertOne(req.body, (err, result) => {
        if (err) return console.log(err);

        console.log('saved to database');
        res.redirect('/')
    });
});
router.get('/', (req, res) => {
    db.collection('data').find().toArray(function(err, results) {
        console.log(results);
        // send HTML file populated with quotes here
        res.render('data', {info: results});
    });

});

module.exports = router;
