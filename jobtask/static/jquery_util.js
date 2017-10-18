function get_init_style()
{
	var init_style = {
		"position":"absolute",
		"padding":"5px",
		"-webkit-border-radius": "8px",
		"-webkit-border-top-left-radius": "0",
		"-moz-border-radius": "8px",
		"-moz-border-radius-topleft": "0",
		"border-radius": "8px",
		"border-top-left-radius": "0",
		"background-color":"#ffffff",
		"border":"1px solid #000000"
	};
	return init_style;
}

function show_simple_tip_ex(selecter,content,container_css)
{
	var x = 10;  
    var y = 20;
    $(selecter).each(function(){
	    $(this).mouseover(function (e) 
	    {
	    	if(this.title)  //如果是超链接
	    	{ 
	    		this.myTitle = content; this.title = "";
	    	}
	    	var tt = this.myTitle?this.myTitle:content;
	    	var init_style = get_init_style();
	    	var container = "<div id='tooltip_system_container'>";
	    	container += tt;
	    	container += "<\/div>";
	        $("body").append(container); //把它追加到文档中
	        $("#tooltip_system_container").css(init_style);
	        if(container_css)
	        {
	        	//console.info(container_css);
	        	$("#tooltip_system_container").css(container_css);
	        }
	        $("#tooltip_system_container").css({  
	            "top": (e.pageY + y) + "px",  
	            "left": (e.pageX + x) + "px"  
	        }).show("fast");   //设置x坐标和y坐标，并且显示  
	    }).mouseout(function () 
	    {  
	    	if(this.title){this.title = this.myTitle;}
	        $("#tooltip_system_container").remove();   //移除 
	    }).mousemove(function (e) 
	    {  
	        $("#tooltip_system_container")  .css({ "top": (e.pageY + y) + "px", "left": (e.pageX + x) + "px" })  
	    });  
    });
}

/*
 * 不依赖jquery的combobox控件
 */
function load_data_for_select(options)
{
	var selector = options.selector || undefined;
	var url = options.url || undefined;
	var disp_fd = options.disp_fd || undefined;
	var val_fd = options.val_fd || undefined;
	// 非必须或可使用默认值
	var value = options.value || undefined;  // for selected
	var callback = options.callback || undefined;
	var condition = options.condition || undefined;
	var is_multiable = options.is_multiable || false; //是否多选
	//如果是多选，则以val_split字符分割之，适配多值的情况
	var val_split = options.val_split || /;|,/ ;  
	var ds_key = options.ds_key || "dataset";

	var post_data = new Object();
	for(var fd  in condition){
		if(typeof(condition[fd]) != "function"){
			post_data[fd] = condition[fd];
		}
	}

	$.ajax(url,{
		data: post_data,
		success: function(jsonobj){
			var $obj = $(''+selector);
			$obj.text('');
			$obj.find("option").remove();  //清除原来的数据
			 if($obj.length>0){
				 //console.info(jsonobj);
				 var dataset = jsonobj[ds_key];
				 //console.info(dataset);
				 if(undefined === value || "" === value){
					 value = $obj.attr("val"); //自定义属性
				 }
				 var vals = new Array();
				 if(is_multiable == false){
					 vals = new Array(value);
				 }else{
					 vals = value.split(val_split);
				 }
				 //console.info(vals);
				 
				 for(idx in dataset){
					 item = dataset[idx];
					 if(disp_fd in item && val_fd in item){
						 var disp = item[disp_fd];
						 var val = item[val_fd];
						 opt = '<option value="#VAL" >#DISP</option>';
						 for(idx2 in vals){
							 //console.info(vals[idx2]+"??"+val);
							 if(vals[idx2] === String(val)){opt = '<option value="#VAL" selected="selected">#DISP</option>';break;}
						 }
						 opt = opt.replace("#VAL", val).replace("#DISP", disp);
						 $obj.append(opt);
					 }
				 }
			}
			 if(typeof(callback) == "function"){callback();}
		},
		error:function(){console.info(this);},
		type: 'post',
		timeout: 3000,
		statusCode: {
			404: function(respobj) {
				console.info(respobj);
			},
			500: function(respobj){
				console.info(respobj);
			}
		}
	});
	return $(""+selector);
}

/*
 * 不依赖jquery的combobox控件
 */
function load_data_for_select_v1(selector, url, condition, display_fd, val_fd, value, extra_options, callback)
{
	var post_data = new Object();

	for(var fd  in condition){
		if(typeof(condition[fd]) != "function"){
			post_data[fd] = condition[fd];
		}
	}

	$.ajax(url,{
		data: post_data,
		success: function(jsonobj){
			var $obj = $(''+selector);
			$obj.text('');
			$obj.find("option").remove();  //清除原来的数据
			 if($obj.length>0){
				 //console.info(jsonobj);
				 var dataset = jsonobj["dataset"];
				 //console.info(dataset);
				 if(undefined === value || "" === value){
					 value = $obj.attr("val"); //自定义属性
				 }
				 for(idx in dataset){
					 item = dataset[idx];
//					 console.info(item);
//					 console.info(display_fd);
//					 console.info(val_fd);

					 if(display_fd in item && val_fd in item){
						 var disp = item[display_fd];
						 var val = item[val_fd];
						 opt = '<option value="#VAL" >#DISP</option>';
						 //console.info(value+"??"+val);
						 if(value === String(val)){opt = '<option value="#VAL" selected="selected">#DISP</option>';}
						 opt = opt.replace("#VAL", val).replace("#DISP", disp);
						 $obj.append(opt);
					 }
				 }
			}
			 if(typeof(callback) == "function"){callback();}
		},
		error:function(){console.info(this);},
		type: 'post',
		timeout: 3000,
		statusCode: {
			404: function(response_obj) {
				var resp_text = response_obj.responseText;
				console.info("[url: " + url + "] Page Not Found !\n\n" + resp_text);
				//alert("[url: " + url + "] Page Not Found !\n\n" + resp_text);
			},
			500: function(response_obj){
				var resp_text = response_obj.responseText;
				console.info("[url: " + url + "] Internal Server Error !\n\n" + resp_text);
				//alert("[url: " + url + "] Internal Server Error !\n\n" + resp_text);
			}
		}
	});
	
	return $(""+selector);
}


function get_mask_style(){
	var mask = {
		"position":"absolute",
		"top":"0px",
		"filter": "alpha(opacity=60)",
		"background-color": "777",
		"z-index": "1002",
		"left": "0px",
		"opacity": "0.5",
		"-moz-opacity": "0.5",
	};
	return mask;
}

/*
 * 
 * */
function load_ajax_data(url, post_data, success_fn, type, dataType)
{
	var type = type || "post";
    var dataType = dataType || "json";
	var post_data = post_data || {};
	if(!success_fn) {success_fn=function(){console.info("not success fn");};}
	
	$.ajax(url,{
		type: type,
		dataType: dataType,
		data: post_data,
//		success: function(data,status){},
		beforeSend: function(){  //开始loading
			var container = "<div class='ajax_loading'>";
	    	container += "loading...";
	    	container += "<\/div>";
	        $("body").append(container); //把它追加到文档中
			$("div.ajax_loading:first").css(get_mask_style());
			$("div.ajax_loading:first").css("height",$(document).height());
			$("div.ajax_loading:first").css("width",$(document).width());
			$("div.ajax_loading:first").show();
		},
		complete: function(){   //结束loading
			$("div.ajax_loading:first").remove();
		},
		success:success_fn,
		error:function(){console.info(this);},
		timeout: 60000,
		statusCode: {
			404: function(response_obj) {
				var resp_text = response_obj.responseText;
				//alert("Error\n\n"+"<h4>url: " + url + "</h4>\n\n"+resp_text);
				console.info("Error\n\n"+"<h4>url: " + url + "</h4>\n\n"+resp_text);
			},
			500: function(response_obj){
				var resp_text = response_obj.responseText; 
				//alert("Error\n\n"+"<h4>url: " + url + "</h4>\n\n"+resp_text);
				console.info("Error\n\n"+"<h4>url: " + url + "</h4>\n\n"+resp_text);
			}
		}
	});
}


function set_selected(selector,value)
{
	$(""+selector).children().each(function(){
		if ($(this).attr("value") == value){
			$(this).attr("selected","selected"); 
		}
	});
}

function get_input_map(selector)
{
	var $cont = $(""+ selector);
	var postdata = {};
	$cont.find("input,textarea,select").each(function(){
		var name = $(this).attr("name");
		//console.info(name);
		var id = $(this).attr("id");
		var val = $(this).val();
		var key = name;
		if(undefined == name || "" == name){
			key = id;
		}
		if(undefined != key && "" != key){
			postdata[name] = val;
		}
	});
	return postdata;
}