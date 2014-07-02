a= {}
b = []
dict = {}
wordList  = []
var socket = io.connect('http://localhost');

function processData(data){
	data = data.toString('utf8')
	spl = data.split('\n');
	c = spl.map(function(element){
		a = {}
		actions = element.split('\t')
		if(actions.length === 2){
			a['start'] = actions[0] 
			a['end']  = actions[1]
			a['frequency'] = 1
			a2 = (a['start'] +  " "  + a['end']).split(' ');
			chosen = wordList.filter(function(n) {
				return a2.indexOf(n) != -1
			});
			a['words'] = chosen
			return a
		}
	});
	c = c.filter(function(n){ return n != undefined });
	c = c.filter(function (element1){
		var keep = true
		for(var i = 0; i < b.length ; i++){
			var element2 = b[i]
			if((element1['start'] === element2['start']) && (element1['end'] === element2['end'])){
				element2['frequency'] += 1
				return false
			}
		}
		return true
	});
	b = b.concat(c)
}

function compareByFreq(a,b) {
	if (a.frequency < b.frequency)
		return 1;
	if (a.frequency > b.frequency)
		return -1;
	return 0;
}


function saveWordList(){
	wordList  = $('#words').val().toString('utf8').split(' ')
}

function showCard(obj){
	var start = obj['start']
	var end = obj['end']
	var freq = obj['frequency']
	var words = JSON.stringify(obj['words'])
	$('#response').append('<div class = "card">' + '<div class = "start">' + start + '</div> <div class = "end">'  + end + '</div><div class =  "freq">' + freq + '</div> <div class = "words"> ' + words + '</div></div>')
}

function showCards(arr){
	$('#response').empty()
	arr.sort(compareByFreq);
	l = arr.length
	for(var i =0 ; i < Math.min(10, l); i++){
		showCard(arr[i])	
	}
	//arr.forEach(showCard);
}

$('#wl').submit(function(event){
	saveWordList()
	$.ajax({
		type: "POST",
		url: "/createwordlist",
       data: $("#wl").serialize() // serializes the form's elements.
   });
	socket.emit('wlsubmit')
	return false
});

socket.on('res', function(d2){
	processData(d2)
	/*f = b.filter(function(element){
		if(element['frequency'] > 1) return true
			return false
	});
	*/
	showCards(b)
	//$('#response').text(JSON.stringify(f));
});

socket.on('err', function(data){
	$('#err').text(JSON.stringify(data));
})
