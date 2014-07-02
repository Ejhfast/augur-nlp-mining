var routes = require('./routes/index');
var users = require('./routes/users');
var path = require('path');
var express = require('express')
var app = express();
var server = require('http').Server(app);
var io = require('socket.io')(server);
app.set('port', process.env.PORT || 3000);
var favicon = require('static-favicon');
var logger = require('morgan');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');
var spawn = require('child_process').spawn;
var exec = require('child_process').exec;
var fs = require('fs');


app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');

app.use(favicon());
app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded());
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

server.listen( app.get('port'), function(){
    console.log("Server listening on " + app.get('port'))
});

app.use('/main', routes);
app.use('/users', users);
app.post('/createwordlist', function(req, res){
    wordliststring = req.body.words.toString('utf8')
    fs.writeFileSync("./wh-dynam.txt", wordliststring)
    console.log("The file was saved!");
    res.send(200) 
});

/// catch 404 and forward to error handler
app.use(function(req, res, next) {
    var err = new Error('Not Found');
    err.status = 404;
    next(err);
});

/// error handlers

// development error handler
// will print stacktrace
if (app.get('env') === 'development') {
    app.use(function(err, req, res, next) {
        res.status(err.status || 500);
        res.render('error', {
            message: err.message,
            error: err
        });
    });
}

// production error handler
// no stacktraces leaked to user
app.use(function(err, req, res, next) {
    res.status(err.status || 500);
    res.render('error', {
        message: err.message,
        error: {}
    });
});



io.on('connection', function (socket) {
    socket.on('wlsubmit', function(){
        //var prefilter = spawn('python', ['../process/prefilter.py', '../files/watpad.tsv']);
        //var filter = spawn('python', ['../process/filter-actions.py', './wh-dynam.txt']);
        //var skip = spawn('ruby', ['../process/skip-gram.rb']);
        //var count = spawn('python', ['../process/count-grams.py', '2']);

        var overview = spawn("sh", ["./overview.sh"])

        /*
        prefilter.stdout.on('data', function (data) {
        filter.stdin.write(data);
        });

        filter.stdout.on('data', function (data) {
        skip.stdin.write(data);
        });

        skip.stdout.on('data', function (data) {
        //count.stdin.write(data);
            data = data.toString('utf8')
            socket.emit('res', data)
            console.log(data)
        });
        
        count.stderr.on('data', function (data) {
        });

        filter.stderr.on('data', function (data) {
        console.log(data.toString('utf8'));
        });
        */

        overview.stderr.on('data', function (data) {
            data = data.toString('utf8');
            console.log(data)
            socket.emit('err', data)    
        });

        overview.stdout.on('data', function (data){
            data = data.toString('utf8')
            socket.emit('res', data)
        })   
    });
});