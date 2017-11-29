function qstep(selector){
	$(selector).find("li").each(function(){
		var li = $(this);
		li.attr("class", "current");
		li.attr("");
	});
}

