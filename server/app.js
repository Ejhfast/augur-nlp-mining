var routes = require('./routes/index');
var users = require('./routes/users');
var path = require('path');
var express = require('express');
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
app.use(express.static(__dirname));


server.listen(app.get('port'), function () {
    console.log("Server listening on " + app.get('port'));
});

app.use('/main', routes);
app.use('/users', users);
app.post('/createwordlist', function (req, res) {
    var wordliststring = req.body.words.toString('utf8');
    fs.writeFileSync("./wh-dynam.txt", wordliststring);
    console.log("The file was saved!");
    res.send(200);
});

/// catch 404 and forward to error handler
app.use(function (req, res, next) {
    var err = new Error('Not Found');
    err.status = 404;
    next(err);
});

/// error handlers

// development error handler
// will print stacktrace
if (app.get('env') === 'development') {
    app.use(function (err, req, res, next) {
        res.status(err.status || 500);
        res.render('error', {
            message: err.message,
            error: err
        });
    });
}

// production error handler
// no stacktraces leaked to user
app.use(function (err, req, res, next) {
    res.status(err.status || 500);
    res.render('error', {
        message: err.message,
        error: {}
    });
});



io.on('connection', function (socket) {
    socket.on('wlsubmit', function () {
        var linecount = 0,
            filename = '../files/sample.tsv';
        
        exec('wc -l ' + filename, function (error, stdout, stderr) {
            var s = stdout;
            linecount = parseInt(stdout.trim().split(' ')[0]);
            console.log(linecount);
            socket.emit('count', linecount);
            if (error !== null) {
                console.log('exec error: ' + error);
            }
        });

        var prefilter = spawn('python', ['../process/prefilter.py', filename]),
            filter = spawn('python', ['../process/filter-actions.py', './wh-dynam.txt']),
            skip = spawn('python', ['../process/skip-gram.py']);
        
        prefilter.stdout.on('data', function (data) {
            filter.stdin.write(data);
        });

        filter.stdout.on('data', function (data) {
            skip.stdin.write(data);
        });

        filter.stderr.on('data', function (data) {
            data = data.toString('utf8');
            console.log(data);
            socket.emit('err', data);
        });

        skip.stdout.on('data', function (data) {
            data = data.toString('utf8');
            socket.emit('res', data);
        });
    });
});