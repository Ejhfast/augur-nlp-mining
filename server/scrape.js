var cheerio = require('cheerio');
var request = require('request');
var fs = require('fs');
var prettyjson = require('prettyjson');
var $;

function getSubheadingContent(obj){
	var arr = [];
	$(obj).find('div > div > ol > li > b').each(function() {
		var txt = $(this).text().replace(/(\r\n|\n|\r)/gm,"");
		if(txt !== ""){
			arr.push(txt);
		}
	});
	return arr;
}

//extract method name
function getSubheadingTitle(obj){
	var subtitle = $(obj).find('span.mw-headline').text();
	return subtitle;
}

//extract Title: How to
function getTitle(obj){
	return $(obj).text();
}

//extract sections
function getSections(obj){
	var arr2 = [];
	$(obj).find('.section').each(function(){
		var subtitle = getSubheadingTitle(this);
		var content = getSubheadingContent(this);
		if(subtitle !== "" && content.length >1){
			arr2.push({"subheading": subtitle, "content": content});
		}
	});
	return arr2;
}

//object contains a title and parts
function getObject(bodyObj){
	var object = {};
	object.parts = [];
	$(bodyObj).find('div > div > div > h1 > a').each(function(){	
		object.title = getTitle(this);
		object.parts = getSections(bodyObj);
	});
	return object;
}

function getObjects($){
	var objects = [];
	$('body').each(function(){
		var object = getObject(this);
		objects.push(object);
	});
	return objects;
}

function extractHowToPage(file){
	$ = cheerio.load(fs.readFileSync(file));
	var objects = getObjects($);
	console.log(prettyjson.render(objects));
}

function getLinksFromCategoriesPage(file, callback){
	var a = [];
	$ = cheerio.load(fs.readFileSync('samp3.html'));
	$('tr > td > div > a').each(function(){
		a.push($(this).attr('href'));
	});
	callback(a);
}

function downloadPages(){
	getLinksFromCategoriesPage(function(a){
		a.forEach(function(elem){
			request(
				{uri: elem}, function(err, response, body){
					fs.appendFileSync("alot.html", body);
				});
		});
	});
}

extractHowToPage('alot.html');