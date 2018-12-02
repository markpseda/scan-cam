var express = require('express');
var router = express.Router();

/* GET data listing. */
router.get('/', function(req, res, next) {
    res.send('Where my data at?');
});

module.exports = router;
