(function run() {
	var title = document.getElementsByClassName('logo')[0].title;
	setInterval(function(){
		console.log(title);
	}, 1000);
})();
