function get_url(){
	return window.location.href;
}

function get_uri(){
	return window.location.pathname;
}

function go(url){
	window.location.href = url;
}

function get_query_from_url(param) {
	var query = location.search; //获取url中"?"符后的字串
	var str = "";
	if (query.indexOf("?") != -1) {  //判断是否有参数
		str = query.substr(1); //从第一个字符开始 因为第0个是?号 获取所有除问号的所有符串
	}
	//没有指定取具体哪个参数，则返回所有的查询字符串
	if(undefined == param || "" == param){
		return str
	}
	strs = str.split("&");
	for(idx in strs){
		key_val = strs[idx].split("=");
		if(key_val[0] == param){
			return key_val[1];  // 找到则直接返回
		}
	}
	return undefined;
}

function get_query_map() {
	var query = location.search; //获取url中"?"符后的字串
	var str = "";
	if (query.indexOf("?") != -1) {  //判断是否有参数
		 str = query.substr(1); //从第一个字符开始 因为第0个是?号 获取所有除问号的所有符串
	}
	map = {}
	strs = str.split("&");
	for(idx in strs){
		key_val = strs[idx].split("=");
		map[key_val[0]] = key_val[1];
	}
	return map;
}

function get_query(){
	return get_query_from_url();
}

//判断元素是否在数组中
function contains(array, element) {
    for (var i = 0; i < array.length; i++) {
        if (array[i] === element) {
            return true;
        }
    }
    return false;
}
    
function to_query_str(obj, excludes){
	var str = "";
	for(var k in obj){
		if( (excludes instanceof Array) &&  contains(excludes, k) == true) {continue;}
		str = str+k+"="+obj[k]+"&";
	}
	str = str.substring(0,str.length-1);
	return str;
}

function trim(str){
	return str.replace(/(^\s*)(\s*$)/g, "");
}

function ltrim(str){
    return str.replace(/(^\s*)/g,"");
}

function rtrim(str){
     return str.replace(/(\s*$)/g,"");
}

function load_style(url){
    var link_tag = document.createElement ("link");
    link_tag.href = url;
    link_tag.rel = "stylesheet";
    var head = document.getElementsByTagName ("head")[0];
    head.appendChild (link_tag);
}

function load_script(url){
    var oHead = document.getElementsByTagName('HEAD').item(0);
    var oScript= document.createElement("script");
    oScript.type = "text/javascript";
    oScript.src=url;
    oHead.appendChild( oScript); 
}

function str_pad_left(str,pad,count){
    while(str.length<count){
        str = pad+str;
    }
    return str;
}

function str_pad_right(str,pad,count){
    while(str.length<count){
        str = str+pad;
    }
    return str;
}

//return like '2013-03-01 12:25:33'
function get_datetime(){
	var td = new Date();
	var y = td.getYear()+1900;
	var m = td.getMonth()+1;
	var d = td.getDate();
	var h = td.getHours();
	var i = td.getMinutes();
	var s = td.getSeconds();
	//y = y<10?("0"+y):y;
	m = m<10?("0"+m):m;
	d = d<10?("0"+d):d;
	h = h<10?("0"+h):h;
	i = i<10?("0"+i):i;
	s = s<10?("0"+s):s;
	return y+"-"+m+"-"+d+" "+h+":"+i+":"+s;
}

//return like '20130301122533'
function get_datetime_str(){
	var td = new Date();
	var y = td.getYear()+1900;
	var m = td.getMonth()+1;
	var d = td.getDate();
	var h = td.getHours();
	var i = td.getMinutes();
	var s = td.getSeconds();
	//y = y<10?("0"+y):y;
	m = m<10?("0"+m):m;
	d = d<10?("0"+d):d;
	h = h<10?("0"+h):h;
	i = i<10?("0"+i):i;
	s = s<10?("0"+s):s;
	return y+m+d+h+i+s;
}

function get_obj_by_json(jsonstr){
	var obj = eval('(' + jsonstr + ')');
	return obj;
}

function from_json(jsonstr)
{
	return get_obj_by_json(jsonstr);
}