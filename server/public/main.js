(function ($,io, window) {
    'use strict';
    // this function is strict...

    $(window).on('load resize', function () {
        $('#header-section').height($(this).innerHeight() - 500);
    });

    var socket = io.connect('http://localhost');

    function compareByFreq(a, b) {
        if (a.frequency < b.frequency) {
            return 1;
        }
        if (a.frequency > b.frequency) {
            return -1;
        }
        return 0;
    }

    function showCards(arr) {
        $('#response').empty();
        arr.sort(compareByFreq);
        for (var i = 0; i < Math.min(100, arr.length); i++) {
            showCard(arr[i]);
        }
    }

    function showCard(obj) {
        var start = obj.start, end = obj.end, freq = obj.frequency, words = JSON.stringify(obj.words);
        $('#start').text(start);
        $('#end').text(end);
        $('#freq').text(freq);
        $('#response').append('<div class="row card"><div id = "start">' + start + '</div><div id = "end">' + end + '</div><div id =  "freq">' + freq + '</div></div>');
    }

    var process = function () {
        var b = [], wordList = [];

        return {
            saveWordList: function () {
                wordList = $('#words').val().toString('utf8').split(' ');
            },
            getArray: function () {
                return b;
            },
            getWordList: function () {
                return wordList;
            },
            processData: function (data) {
                var spl = data.toString('utf8').split('\n');
                var c = spl.map(function (element) {
                    var a = {};
                    var actions = element.split('\t');
                    if (actions.length === 2) {
                        a.start = actions[0];
                        a.end = actions[1];
                        a.frequency = 1;
                        var a2 = (a.start + " " + a.end).split(' ');
                        var chosen = wordList.filter(function (n) {
                            return a2.indexOf(n) !== -1;
                        });
                        a.words = chosen;
                        return a;
                    }
                });
                c = c.filter(function (n) {
                    return n !== undefined;
                });
                c = c.filter(function (element1) {
                    for (var i = 0; i < b.length; i++) {
                        var element2 = b[i];
                        if ((element1.start === element2.start) && (element1.end === element2.end)) {
                            element2.frequency += 1;
                            return false;
                        }
                    }
                    return true;
                });
                b = b.concat(c);
            }
        };
    };

    var p1;
    $('#wl').submit(function () {
        $('.progress-bar').css('width', 0 + '%').attr('aria-valuenow', 0);
        $('#wl').slideToggle(400);

        p1 = process();
        p1.saveWordList();
        $.ajax({
            type : "POST",
            url : "/createwordlist",
            data : $("#wl").serialize() // serializes the form's elements.
        });

        socket.emit('wlsubmit');
        return false;
    });

    var total = 10000;

    socket.on('err', function (data) {
        var j = JSON.stringify(data);
        var k = parseInt(j.split(' ')[1], 10);
        $('.progress-bar').css('width', k / (total / 100) + '%').attr('aria-valuenow', k / (total / 100));
    });

    socket.on('count', function (data) {
        total = data;
    });

    socket.on('doneerr', function () {
        $('.progress-bar').css('width', 100 + '%').attr('aria-valuenow', 100);
        $('#wl').slideToggle(400);
    });
    
    socket.on('res', function (data) {
        p1.processData(data);
        showCards(p1.getArray());
    });
}($,io,window));