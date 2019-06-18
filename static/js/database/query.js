function setAceEditMode(ids,model,theme) {
	try
	  {
		var editor = ace.edit(ids);
		require("ace/ext/old_ie");
		var langTools = ace.require("ace/ext/language_tools");
		editor.removeLines();
		editor.setTheme(theme);
		editor.getSession().setMode(model);
		editor.setShowPrintMargin(false);
		editor.setOptions({
		    enableBasicAutocompletion: true,
		    enableSnippets: true,
		    enableLiveAutocompletion: true
		}); 
	 	return editor
	  }
	catch(err)
	  {
		console.log(err)
	  }

			 
}
function makeRandomId() {
  var text = "";
  var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
  for (var i = 0; i < 8; i++)
    text += possible.charAt(Math.floor(Math.random() * possible.length));
  return text;
}
var webconsole = false
function make_terminal(element, size, ws_url) { 
    var term = new Terminal({
        cols: size.cols,
        rows: size.rows,
        screenKeys: true,
        useStyle: true,
        cursorBlink: true,  // Blink the terminal's cursor
    });         	
    if (webconsole) {
        return;
    }        
    webconsole = true;        	
    term.open(element, false);
    term.write('正在连接...')
/*             term.fit(); */
    var ws = new WebSocket(ws_url);
    ws.onopen = function (event) {
        term.resize(term.cols, term.rows);
/*                 ws.send(JSON.stringify(["id", id,term.cols, term.rows]));  */
        term.on('data', function (data) {
            <!--console.log(data);-->
             ws.send(data); 
        });

        term.on('title', function (title) {
            document.title = title;
        });
        ws.onmessage = function (event) {
        	term.write(event.data);
        };      
    };
    ws.onerror = function (e) {
    	term.write('\r\n连接失败')
    	ws = false
    };
/*    ws.onclose = function () {
        term.destroy();
    }; */     
    return {socket: ws, term: term};
}
function customMenu(node) {
      var items = {
              "new":{  
                  "label":"查询数据",  
                  "icon": "glyphicon glyphicon-plus",
                  "action":function(data){
                  	var inst = $.jstree.reference(data.reference),
						obj = inst.get_node(data.reference);
						querySQL(obj);
                  }  
              },           
              "monitor":{
            		"separator_before"	: false,
					"separator_after"	: false,
					"_disabled"			: false, 
					"label"				: "监控信息",
					"shortcut_label"	: 'F2',
					"icon"				: "fa fa-bar-chart",
					"action"			: function (data) {
						var inst = $.jstree.reference(data.reference),
						obj = inst.get_node(data.reference);
						$.alert({
						    title: '警告!',
						    type: 'red',
						    content: '您无权操作此项',
						});				
					}
            }, 
            "view":{
              		"separator_before"	: false,
					"separator_after"	: false,
					"_disabled"			: false, 
					"label"				: "查看表结构",
					"shortcut_label"	: 'F2',
					"icon"				: "fa fa-search-plus",
					"action"			: function (data) {
						var inst = $.jstree.reference(data.reference),
						obj = inst.get_node(data.reference);
						viewTableSchema(obj)
					}
            },            
            "webconsole":{
        		"separator_before"	: false,
				"separator_after"	: false,
				"_disabled"			: false, 
				"label"				: "终端查询",
				"shortcut_label"	: 'F2',
				"icon"				: "fa fa-terminal",
				"action"			: function (data) {
					var inst = $.jstree.reference(data.reference),
					obj = inst.get_node(data.reference);
					var parents = inst.get_path('#' + obj.parent ,false)
					var parentsName = ''
					for (var i=0; i <parents.length; i++){
						parentsName = parentsName + parents[i].split("(")[0]
					}
					openTerminal(obj,parentsName)				
				}
        }            
	  }
      if(node["id"].indexOf("table_")>=0){
    		try {    
    			delete items.new	  
	    	  	delete items.monitor
	    	  	delete items.webconsole
    		}
    		catch(err) {
    			console.log(err)
    		}     	  
      }else if(node["id"]>100000 && node["id"]<200000){
  		try {
	    	  delete items.view
	    	  delete items.webconsole
		}
		catch(err) {
			console.log(err)
		} 
      }
      return items
}


function drawTree(ids,url){
    $(ids).jstree({	
	    "core" : {
	      "check_callback": function (op, node, par, pos, more) {  	  
	    	    if ((op === "move_node" || op === "copy_node") && node.type && node.id > 10000  && node.id < 30000) {	    	    	
	    	        return false;
	    	    }
	    	    else if ((op === "move_node" || op === "copy_node") && node.id.indexOf("table_")>=0 ) {	
	    	    	return false;
	    	    	
	    	    }
	    	    return true;
	    	},
	      'data' : {
	        "url" : url,
	        "dataType" : "json" // needed only if you do not supply JSON headers
	      }
	    },	    
/*	    "plugins": ["contextmenu", "dnd", "search","themes","state", "types", "wholerow","json_data","unique","checkbox"],*/
	    "plugins": ["contextmenu", "dnd", "search","themes","state", "types", "wholerow","json_data","unique"],
/*        "checkbox": {
            "keep_selected_style": false,//是否默认选中
            "three_state": false,//父子级别级联选择
            "tie_selection": false
        },*/	    
	    "contextmenu":{
		    	select_node:false,
		    	show_at_node:true,
		    	'items': customMenu
		      }	    
	});		
}


$(document).ready(function () {

	try{
		var aceEditAdd = setAceEditMode("compile-editor-add","ace/mode/mysql","ace/theme/sqlserver");								 		  
	}
	catch(err){
		console.log(err)
	}		
	
	drawTree('#dbTree',"/api/db/tree/")
	
    $("#search-input").keyup(function () {
        var searchString = $(this).val();
        $('#dbTree').jstree('search', searchString);
    });	
	
	function sleep(){
		alert("1")
		return false
	}
	
    $("#dbTree").click(function () {
        var position = 'last';
        var parent = $("#dbTree").jstree("get_selected");
        if (parent[0] > 100000 && parent[0] < 200000){
        	$("#dbTree").jstree("open_node", parent[0]);
            var dbId = parent[0]-100000
        	$.ajax({  
                cache: true,  
                type: "POST",  
                url:"/db/manage/", 
                data:{
                	"model": "table_list",
                	"db":dbId
                },
                async : false,  
	            error: function(response) {
	            	new PNotify({
	                    title: 'Ops Failed!',
	                    text: response.responseText,
	                    type: 'error',
	                    styling: 'bootstrap3'
	                });       
	            },  
	            success: function(response) {  
					if(response["code"]==500){
			           	new PNotify({
			                   title: 'Ops Failed!',
			                   text: response["msg"],
			                   type: 'error',
			                   styling: 'bootstrap3'
			            }); 					
					}else{
		            	let respone = response["data"]		            	       	        	  
						for (var i=0; i <respone.length; i++){				    
	                        var newNode = {
	                        		"id":"table_"+ dbId +"_" + i,
	                                "text": respone[i],
	                                "icon": "fa fa-bar-chart assets-online"
	                            }                            						
							;	
	                        $('#dbTree').jstree('create_node', parent, newNode, position, false, false)
	                        if (i>1000){
	                        	break
	                        }
//	                        var s = i % 1000
//							if(s == 0){
//								setTimeout('console.log("Wait draw table list")',100)
////								console.log(i,s)
//							}
						}
						$("#dbTree").jstree("open_node", parent); 
					}	            	
	            } 
        	});                    
        }
    });	
    
	$("#db_query_btn").on('click', function() {
		var btnObj = $(this);
		btnObj.attr('disabled',true); 
		var db = $(this).val()
		console.log(db)
		if (db > 0){
			$('#show_sql_result').show();		
			var sql = aceEditAdd.getSession().getValue();
		    if ( sql.length == 0 || db == 0){
		    	new PNotify({
		            title: 'Warning!',
		            text: 'SQL内容与数据库不能为空',
		            type: 'warning',
		            styling: 'bootstrap3'
		        }); 
		    	btnObj.removeAttr('disabled');
		    	return false;
		    };			
			$.ajax({
				url:'/db/manage/', 
				type:"POST",  
				"dateType":"json",			
				data:{
					"db":db,
					"model":'query_sql',
					"sql":sql
				},  //提交参数
				success:function(response){
					btnObj.removeAttr('disabled');
					var ulTags = '<ul class="list-unstyled timeline widget">'	
					var tableHtml = ''
					var liTags = '';
					var tablesList = [];
					if (response['code'] == "200" && response["data"].length > 0 ){
						for (var i=0; i <response["data"].length; i++){
							var tableId = "query_result_list_"+ i
							tablesList.push(tableId)
							if (response["data"][i]["dataList"][0] >= 0){
								var tableHtml = '<table class="table" id="'+ tableId +'"><thead><tr>'
								var trHtml = '';
								for (var x=0; x <response["data"][i]["dataList"][2].length; x++){
									trHtml = trHtml + '<th>' + response["data"][i]["dataList"][2][x] +'</th>';
								}; 	
								tableHtml = tableHtml + trHtml + '</tr></thead><tbody>';
								var trsHtml = '';
								for (var y=0; y <response["data"][i]["dataList"][1].length; y++){
									var tdHtml = '<tr>';
									for (var z=0; z < response["data"][i]["dataList"][1][y].length; z++){
										tdHtml = tdHtml + '<td>' + response["data"][i]["dataList"][1][y][z]  +'</td>';
									} 	
									trsHtml = trsHtml + tdHtml + '</tr>';
								}                    	
								tableHtml = tableHtml + trsHtml +  '</tbody></table>';														
							}else{
								tableHtml = response["data"][i]["dataList"]

							}
			
						}
						$("#result").html(tableHtml);
					    if (tablesList.length) {
					    	for (var i=0; i <tablesList.length; i++){
							   var table = $("#"+tablesList[i]).DataTable( {
							        dom: 'Bfrtip',
							        "lengthMenu": [ [50, 150, 450, -1], [50, 150, 450, "All"] ],
							        buttons: [{
						                    extend: "copy",
						                    className: "btn-sm"
						                },
						                {
						                    extend: "csv",
						                    className: "btn-sm"
						                },
						                {
						                    extend: "excel",
						                    className: "btn-sm"
						                },
						                {
						                    extend: "pdfHtml5",
						                    className: "btn-sm"
						                },
						                {
					                    extend: "print",
						                    className: "btn-sm"
						            }],
									language : {
										"sProcessing" : "处理中...",
										"sLengthMenu" : "显示 _MENU_ 项结果",
										"sZeroRecords" : "没有匹配结果",
										"sInfo" : "显示第 _START_ 至 _END_ 项结果，共 _TOTAL_ 项",
										"sInfoEmpty" : "显示第 0 至 0 项结果，共 0 项",
										"sInfoFiltered" : "(由 _MAX_ 项结果过滤)",
										"sInfoPostFix" : "",										
										"sSearch" : "搜索:",
										"sUrl" : "",
										"sEmptyTable" : "表中数据为空",
										"sLoadingRecords" : "载入中...",
										"sInfoThousands" : ",",
										"oPaginate" : {
											"sFirst" : "首页",
											"sPrevious" : "上页",
											"sNext" : "下页",
											"sLast" : "末页"
										},
										"oAria" : {
											"sSortAscending" : ": 以升序排列此列",
											"sSortDescending" : ": 以降序排列此列"
										}
								},					            
							   });	
							}				    		
					    }						
						}
					else{
						var selectHtml = '<div id="result">' + response["msg"] + '</div>';
						$("#result").html(selectHtml);						
					}		                								
				},
		    	error:function(response){
		    		btnObj.removeAttr('disabled');
		           	new PNotify({
		                   title: 'Ops Failed!',
		                   text: response.responseText,
		                   type: 'error',
		                   styling: 'bootstrap3'
		            }); 
		    	}
			});			
		}
	});    
    
})


function querySQL(obj){
	if (obj["id"]>=100000){
		console.log(obj["text"])
		$("#dbChoice").html(" <code>"+obj["text"]+"</code>")
		$("#db_query_btn").removeClass("disabled").text("查询").val(obj["id"]-100000)	
	}else{
		$.alert({
		    title: '警告!',
		    type: 'red',
		    content: '暂无更多信息',
		});			
	}
}

function viewTableSchema(obj){
	if (obj["id"].indexOf("table_")>=0){
		var aId = obj["id"].split("_")
    	$.ajax({  
            cache: true,  
            type: "POST",    
            async: false,
            url:"/db/manage/",
            data:{
            	"model": "table_schema",
            	"db": aId[1],
            	"table_name":obj["text"]
            }, 
            error: function(response) {
            	new PNotify({
                    title: 'Ops Failed!',
                    text: response.responseText,
                    type: 'error',
                    styling: 'bootstrap3'
                });       
            },  
            success: function(response) {  	
				if(response["code"]==500){
		           	new PNotify({
		                   title: 'Ops Failed!',
		                   text: response["msg"],
		                   type: 'error',
		                   styling: 'bootstrap3'
		            }); 					
				}else{
				var schemaTableHtml = '<table class="table table-striped">' +		                
							              '<tbody>' +
							                '<tr>' +
							                  '<td>数据库: </td>' + '<td>'+ response["data"]["schema"][1][0][0] +'</td>' +
							                  '<td>表名: </td>' +	'<td>'+ response["data"]["schema"][1][0][1] +'</td>' +
							                  '<td>表类型: </td>' + '<td>'+ response["data"]["schema"][1][0][2] +'</td>' +	
							                '</tr>' +
							                '<tr>' +  
							                  '<td>存储引擎: </td>' + '<td>'+ response["data"]["schema"][1][0][3] +'</td>' +	
							                  '<td>版本: </td>' + '<td>'+ response["data"]["schema"][1][0][4] +'</td>' +						
							                  '<td>行格式: </td>' + '<td>'+ response["data"]["schema"][1][0][5] +'</td>' +		
							                '</tr>' +  
							                '<tr>' +  
							                  '<td>行记录数: </td>' + '<td>'+ response["data"]["schema"][1][0][6] +'</td>' +	
							                  '<td>数据长度: </td>' + '<td>'+ response["data"]["schema"][1][0][7] +'</td>' +		
							                  '<td>最大数据长度: </td>' + '<td>'+ response["data"]["schema"][1][0][8] +'</td>' +	
								            '</tr>' +	
								            '<tr>' + 
							                  '<td>索引长度: </td>' + '<td>'+ response["data"]["schema"][1][0][9] +'</td>' +	
							                  '<td>数据空闲: </td>' + '<td>'+ response["data"]["schema"][1][0][10] +'</td>' +	
							                  '<td>自动递增值: </td>' + '<td>'+ response["data"]["schema"][1][0][11] +'</td>' +	
									        '</tr>' +	
									        '<tr>' + 							                  
							                  '<td>创建日期: </td>' + '<td>'+ response["data"]["schema"][1][0][12] +'</td>' +	
							                  '<td>字符集类型: </td>' + '<td>'+ response["data"]["schema"][1][0][13] +'</td>' +	
							                  '<td>注释</td>' + '<td>'+ response["data"]["schema"][1][0][14] +'</td>' +	
							                '</tr>'	 +                       
							              '</tbody>' +
							           '</table>'                    					
				var indexTableHtml = '<table class="table table-striped"><thead><tr>'     	
				    var indexTrHtml = '';
					for (var i=0; i <response["data"]["index"][2].length; i++){
						indexTrHtml = indexTrHtml + '<th>' + response["data"]["index"][2][i] +'</th>';
					}; 
					indexTableHtml = indexTableHtml + indexTrHtml + '</tr></thead><tbody>';
					var indexHtml = '';
					for (var i=0; i <response["data"]["index"][1].length; i++){
						var indexTdHtml = '<tr>';
						for (var x=0; x < response["data"]["index"][1][i].length; x++){
							indexTdHtml = indexTdHtml + '<td>' + response["data"]["index"][1][i][x] +'</td>';
						} 	
						indexHtml = indexHtml + indexTdHtml + '</tr>';
					}                    	
				indexTableHtml = indexTableHtml + indexHtml +  '</tbody></table>';						
				var descHtml = '<pre><code class="sql hljs">' + response["data"]["desc"] + '<br></code></pre>';	
                var schemaHtml = '<div id="schema_result"><ul class="list-unstyled timeline widget">' +
					               '<li>' +
					                '<div class="block">' +
					                  '<div class="block_content">' +
					                    '<h2 class="title">' +
					                       '<a>表结构信息</a>' +
					                    '</h2><br>' +
					                    schemaTableHtml +
					                  '</div>' +
					                '</div>' +
					              '</li>' +
					              '<li>' +
					               '<li>' +
					                '<div class="block">' +
					                  '<div class="block_content">' +
					                    '<h2 class="title">' +
					                       '<a>表索引信息</a>' +
					                    '</h2><br>' +
					                    indexTableHtml +
					                  '</div>' +					                  
					                '</div>' +
					              '</li>' +
					               '<li>' +
					                '<div class="block">' +
					                  '<div class="block_content">' +
					                    '<h2 class="title">' +
					                       '<a>DDL信息</a>' +
					                    '</h2><br>' +					                    
					                    descHtml +
					                  '</div>' +
					                '</div>' +
					              '</li>' +					              
					            '</ul>'				
				$("#schema_result").html(schemaHtml); 
			    $('pre code').each(function(i, block) {
			    	hljs.highlightBlock(block);
			  	});	
					}                    	
            }
        });	
	}else{
		$.alert({
		    title: '警告!',
		    type: 'red',
		    content: '暂无更多信息',
		});		
	}	
}
 