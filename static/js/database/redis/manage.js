var webssh = false
var curr_line = '';
function make_terminal(element, size, ws_url, local_cli) { 
    var term = new Terminal({
        cols: size.cols,
        rows: size.rows,
        screenKeys: true,
        useStyle: true,
        cursorBlink: true,  // Blink the terminal's cursor
    });    
    
    if (webssh) {
        return;
    }     
    
    webssh = true;        	
    term.open(element, false);
    term.writeln('\033[33m \r\nWelcome to Redis web terminal.\033[0m');
	term.prompt = () => {
	    term.write("\r\n"+local_cli);
	};
	
    var ws = new WebSocket(ws_url);
    
    ws.onopen = function (event) {

    	term.prompt();	
    	
        term.resize(term.cols, term.rows);
        
        term.on('key', function(key, ev) {
            const printable = !ev.altKey && !ev.altGraphKey && !ev.ctrlKey && !ev.metaKey;
            //console.log(key.charCodeAt(0))

            if (key.charCodeAt(0) == 3) {
	        	//捕获ctrl+c
            	curr_line = ''
            	term.prompt()
	        }            
            
            if (key.charCodeAt(0) == 27) {
	        	//跳过方向键
	        	return false
	        }
            
            if (ev.keyCode == 13) {                
                if(curr_line.length){
                	ws.send(curr_line)
                }else{
                	term.prompt()
                }           
                curr_line = '';
            } else if (ev.keyCode == 8) {
                if (term.x > 2) {
                    curr_line = curr_line.slice(0, -1);
                    term.write('\b \b');
                }
            } else if (printable) {
                curr_line += ev.key;
                term.write(key);
            } 
                              
        });

        term.on('paste', function(data) {
            term.write(data);            
        	if (curr_line.length){
        		console.log(curr_line)
                ws.send(curr_line + data)        		
        	}else{
        		ws.send(data)
        	}            
            
        });       
        
        term.on('title', function (title) {
            document.title = title;
        });
        
        ws.onmessage = function (event) {
        	term.write("\r\n" + event.data);
        	term.prompt();
        };  
                 
    };
    
    ws.onerror = function (e) {
    	term.write('\r\n连接失败')
    	ws = false
    };   

    ws.onclose = function(e) {
       	new PNotify({
            title: 'Ops Failed!',
            text: "连接断开",
            type: 'error',
            styling: 'bootstrap3'
    	}); 
       	term.writeln('\033[31m \r\n连接已断开，请重新连接 \033[0m');
    };    
    
    return {socket: ws, term: term};
}


var language =  {
		"sProcessing" : "处理中...",
		"sLengthMenu" : "显示 _MENU_ 项结果",
		"sZeroRecords" : "没有匹配结果",
		"sInfo" : "显示第 _START_ 至 _END_ 项结果，共 _TOTAL_ 项",
		"sInfoEmpty" : "显示第 0 至 0 项结果，共 0 项",
		"sInfoFiltered" : "(由 _MAX_ 项结果过滤)",
		"sInfoPostFix" : "",
		"sSearch" : "搜索: ",
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
	}

function make_database_binlog(vIds,select_name){
	switch(select_name) {
	    case "binlog_db_file":
	       var model = "binlog_sql"
	       break;
	    case "table_name":
	    	var model = "table_list"
	       break;
	    case "optimize_db":
	    	var model = "optimize_sql"
	       break;
	}	
	$.ajax({
		url:'/db/redis/manage/', //请求地址
		type:"POST",  //提交类似			
		data:{
			"db":vIds,
			"model":model,
		},  //提交参数
		success:function(response){
            if (response["code"] == 200){
	            if (response["data"].length) {
	    			var selectHtml = '<select required="required" class="selectpicker form-control" data-live-search="true" name="'+select_name+'" id="'+select_name+'"  data-size="10" data-selected-text-format="count > 3"  data-width="100%"  autocomplete="off">' 
	    			var option = '';
	    			for (var i=0; i <response["data"].length; i++){
	    				option = option + '<option value="'+ response["data"][i] +'">'+ response["data"][i] +'</option>'
	    			}													
	    			var selectHtml = selectHtml + option + '</select>';
	    			$("#"+select_name).html(selectHtml);
	    			$('.selectpicker').selectpicker('refresh');	
				}		            
            }else{
	           	new PNotify({
	                   title: 'Ops Failed!',
	                   text: response["msg"],
	                   type: 'error',
	                   styling: 'bootstrap3'
	            }); 	            	
            }                            								
		},
    	error:function(response){
           	new PNotify({
                   title: 'Ops Failed!',
                   text: response.responseText,
                   type: 'error',
                   styling: 'bootstrap3'
            }); 
    	}
	});                           								
}

function requests(method,url,data){
	var ret = '';
	$.ajax({
		async:false,
		url:url, //请求地址
		type:method,  //提交类似
       	success:function(response){
             ret = response;
        },
        error:function(data){
            ret = {};
        }
	});	
	return 	ret
}
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

function InitDataTable(tableId,dataList,buttons,columns,columnDefs){
	  oOverviewTable =$('#'+tableId).dataTable(
			  {
				    "dom": "Bfrtip",
				    "buttons":buttons,				  
		    		"bScrollCollapse": false, 				
		    	    "bRetrieve": true,			
		    		"destroy": true, 
		    		"data":	dataList,
		    		"columns": columns,
		    		"columnDefs" :columnDefs,			  
		    		"language" : language,
		    		"iDisplayLength": 20,
		            "select": {
		                "style":    'multi',
		                "selector": 'td:first-child'
		            },		    		
		    		"order": [[ 0, "ase" ]],
		    		"autoWidth": false	    			
		    	});  	  
}

function RefreshTable(tableId, urlData){
	  $.getJSON(urlData, null, function( dataList )
	  {
	    table = $(tableId).dataTable();
	    oSettings = table.fnSettings();
	    
	    table.fnClearTable(this);

	    for (var i=0; i<dataList.length; i++)
	    {
	      table.oApi._fnAddData(oSettings, dataList[i]);
	    }

	    oSettings.aiDisplay = oSettings.aiDisplayMaster.slice();
	    table.fnDraw();	
	    	    	
	  });
}


function makeDbManageTableList(dataList){
    var columns = [
                   {"data": "db_mark"},
	               {
	            	   "data": "db_name",
	            	   "defaultContent": ""
	               },
	               {"data": "ip"},
	               {"data": "db_port"},	               
	               {"data": "db_rw"}    
	        ]
   var columnDefs = [       		    		        
	    		        {
   	    				targets: [5],
   	    				render: function(data, type, row, meta) {
   	                        return '<div class="btn-group  btn-group-xs">' +	
/*	    	                           '<button type="button" name="btn-database-query" value="'+ row.id +'" class="btn btn-default"  aria-label="Justify"><span class="fa fa-search-plus" aria-hidden="true"></span>' +	
	    	                           '</button>' +*/	
	    	                           '<button type="button" name="btn-database-terminal" value="'+ row.id +'" class="btn btn-default"  aria-label="Justify"><span class="fa fa-terminal" aria-hidden="true"></span>' +	
	    	                           '</button>' +  	    	                           
	    	                           '</div>';
   	    				},
   	    				"className": "text-center",
	    		        },
	    		      ]	
    var buttons = []  
    InitDataTable('UserDatabaseListTable',dataList,buttons,columns,columnDefs);	
}

function customMenu(node) {
      var items = {}
      return items
}


function drawTree(ids,url){
	$(ids).jstree('destroy');
    $(ids).jstree({	
	    "core" : {
	      "check_callback": function (op, node, par, pos, more) {  	  
	    	    if (op === "move_node" || op === "copy_node") {	    	    	
	    	        return false;
	    	    }
	    	    return true;
	    	},
	      'data' : {
	        "url" : url,
	        "dataType" : "json" 
	      }
	    },	    
	    "plugins": ["contextmenu", "dnd", "search","themes","state", "types", "wholerow","json_data","unique"],    
	    "contextmenu":{
		    	select_node:false,
		    	show_at_node:true,
		    	'items': customMenu
		      }	    
	});		
}

function drawTableTree(ids,jsonData){
	$(ids).jstree('destroy');
    $(ids).jstree({	
	    "core" : {
	      "check_callback": function (op, node, par, pos, more) {  	  
	    	    if (op === "move_node" || op === "copy_node") {	    	    	
	    	        return false;
	    	    }
	    	    return true;
	    	},
	      'data' : jsonData
	    },	    
	    "plugins": ["contextmenu", "dnd", "search","themes","state", "types", "wholerow","json_data","unique"],    
	    "contextmenu":{
		    	select_node:false,
		    	show_at_node:true,
		    	'items': {
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
	            }		    		
		    	}
		      }	    
	});		
}


$(document).ready(function () {

	
	var randromChat = makeRandomId()
	         

    if ($("#UserDatabaseListTable").length) {   
    	
    	$('#UserDatabaseListTable tbody').on('click',"button[name='btn-database-terminal']",function(){   
			if(!webssh){
	        	let vIds = $(this).val();
	        	let td = $(this).parent().parent().parent().find("td")
	        	$("#dbChoice").html('<i  class="fa  fa-paper-plane" >数据库  <u class="red">'+ td.eq(1).text() +'</u> 操作入口</i>')
				$("#db_terminal_btn").removeClass("disabled").val(vIds)
				var local_cli= td.eq(2).text() + '[' +td.eq(1).text().replace('db','') + ']> '; 	
				let ws_scheme = window.location.protocol === "https:" ? "wss" : "ws";
				var ws_path = ws_scheme + '://' + window.location.host + '/ws/redis/terminal/'+ vIds + '/' + randromChat + '/'; 			
				websocket = make_terminal(document.getElementById('compile-editor-add'), {rows: 29, cols: 140}, ws_path, local_cli);					
				
			}else{
            	new PNotify({
                    title: 'Ops Failed!',
                    text: "请关闭旧的连接",
                    type: 'error',
                    styling: 'bootstrap3'
                }); 				
			}
        });	     	    	
    }	
	
	drawTree('#dbTree',"/api/db/redis/tree/?db_rw=r/w&db_rw=read&db_rw=write")
	
    $("#search-input").keyup(function () {
        var searchString = $(this).val();
        $('#dbTree').jstree('search', searchString);
    });	
		
    $("#dbTree").click(function () {
	     var position = 'last';
	     let select_node = $(this).jstree("get_selected",true)[0]["original"];
	     if(select_node["last_node"] == 1){
				$.ajax({
					  type: 'GET',
					  url: '/api/db/redis/user/list/?db_server='+ select_node["db_server"],
				      success:function(response){	
				    	  if ($('#UserDatabaseListTable').hasClass('dataTable')) {
				            dttable = $('#UserDatabaseListTable').dataTable();
				            dttable.fnClearTable();
				            dttable.fnDestroy(); 
				    	  }			    	  
				    	  makeDbManageTableList(response)
				      },
		              error:function(response){
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

    $("#db_terminal_btn").on('click', function () { 
		try {
			websocket["socket"].close()
		}
		catch(err) {
			console.log(err)
		} 
		finally {
			webssh = false
		}    	
    }); 
		
})    


function viewTableSchema(obj){
	if (obj["original"]["db"]){
    	$.ajax({  
            cache: true,  
            type: "POST",    
            async: false,
            url:"/db/redis/manage/",
            data:{
            	"model": "table_schema",
            	"db": obj["original"]["db"],
            	"table_name":obj["original"]["text"]
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
				if(response["code"]!=200){
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
 