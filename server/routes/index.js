var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res) {
	console.log( "here")
	res.render('new.jade', { title: 'Augur' });
});

module.exports = router;
