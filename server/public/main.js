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

a= {}
var socket = io.connect('http://localhost');
b = []
socket.on('res', function(d2){
	d2 = processData(d2)
	b.push(d2)
	$('#response').text(JSON.stringify(b));
});