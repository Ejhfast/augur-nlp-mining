var a= {}
var b = []
var wordList  = []
var socket = io.connect('http://localhost');

function processData(data){
    a = {}
    data = data.toString('utf8')
    spl = data.split('\n');
    spl.map(function(element){
        actions = element.split('\t')
        if(actions.length !== 2) return
        a['start'] = actions[0] 
        a['end']  = actions[1]
        a['frequency'] = 1
    })
    return a
}

function saveWordList(){
	wordList  = $('#words').val().toString('utf8').split(' ')
}

$('#wl').submit(function(event){
	saveWordList()
	socket.emit('wlsubmit')
   $.ajax({
       type: "POST",
       url: "/createwordlist",
       data: $("#wl").serialize() // serializes the form's elements.
     });
	return false
});

function displayData(data, type){
	if(type ===1){
		b.push(data)
		$('#response').text(JSON.stringify(b));
	}else{

	}
}

socket.on('res', function(d2){
	d2 = processData(d2)
	displayData(d2, 1)
});
