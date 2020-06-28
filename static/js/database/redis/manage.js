var statusLevelHtml = {
	    "high":'<span class="label label-danger">高</span>',
	    "mid":'<span class="label label-info">中</span>',
	    "low":'<span class="label label-success">低</span> '
	}
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
//	term.prompt = () => {
//	    term.write("\r\n"+local_cli);
//	};
	
    var ws = new WebSocket(ws_url);
    
    ws.onopen = function (event) {

    	//term.prompt();	
    	
        term.resize(term.cols, term.rows);
        
        term.on('key', function(key, ev) {
            const printable = !ev.altKey && !ev.altGraphKey && !ev.ctrlKey && !ev.metaKey;
            //console.log(key.charCodeAt(0))

            if (key.charCodeAt(0) == 3) {
	        	//捕获ctrl+c
            	curr_line = ''
            	//term.prompt()
	        }            
            
            if (key.charCodeAt(0) == 27) {
	        	//跳过方向键
	        	return false
	        }
            
            if (ev.keyCode == 13) {                
                if(curr_line.length){
                	ws.send(curr_line)
                }else{
                	//term.prompt()
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
        	//term.prompt();
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
	if (node["original"]["last_node"]==1){
	    var items = {
	            "show_memory":{  
	                "label":"当前内存情况",  
	                "icon": "fa fa-picture-o",
	                "action":function(data){
	                	var inst = $.jstree.reference(data.reference),
						obj = inst.get_node(data.reference);
	                	show_memory(obj, inst)
	                }  
	            },	    		
	            "show_commands":{  
	                "label":"命令执行情况",  
	                "icon": "fa fa-bar-chart-o",
	                "action":function(data){
	                	var inst = $.jstree.reference(data.reference),
						obj = inst.get_node(data.reference);
	                	show_commands(obj, inst)
	                }  
	            },	    		
	            "show_stats":{  
	                "label":"Redis当前状态",  
	                "icon": "fa fa-pie-chart",
	                "action":function(data){
	                	var inst = $.jstree.reference(data.reference),
						obj = inst.get_node(data.reference);
	                	show_stats(obj, inst)
	                }  
	            }		            
	        }  
	    return items		
	}

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


function drewRedisStatusTables(ids, dataList){
    var columns = [
        {"data": "name"},
        {
     	   "data": "value",
     	   "defaultContent": ""
        },
        {
        	"data": "metric",
        	"defaultContent": " - ",
        	"className": "text-center"
        },
        {
        	"data": "level",
        	"className": "text-center"
        },
        {"data": "desc"},	                 
 ]
	var columnDefs = [  
					{
						targets: [1],
						render: function(data, type, row, meta) {
							if(row.value instanceof Object){
								console.log(row.value.calls)
								return JSON.stringify(row.value)
							}
							return row.value
						},
					},		
					{
						targets: [3],
						render: function(data, type, row, meta) {
							return statusLevelHtml[row.level]
						},
					},		
			      ]	
	var buttons = [	
	] 
	
	InitDataTable(ids,dataList,buttons,columns,columnDefs);	
}

function show_memory(obj, inst){
	let dataList = requests('get','/api/db/redis/status/'+ obj["original"]["db_server"] +'/?type=memory')["data"]
	if ($('#redisMemoryTable').hasClass('dataTable')) {
        dttable = $('#redisMemoryTable').dataTable();
        dttable.fnClearTable();
        dttable.fnDestroy();         
	}	
	drewRedisStatusTables('redisMemoryTable',dataList)
	$("#redisMemoryTable").show()	
}

function show_commands(obj, inst){
	let dataList = requests('get','/api/db/redis/status/'+ obj["original"]["db_server"] +'/?type=cmd')["data"]
	if ($('#redisCommandTable').hasClass('dataTable')) {
        dttable = $('#redisCommandTable').dataTable();
        dttable.fnClearTable();
        dttable.fnDestroy();         
	}	
	drewRedisStatusTables('redisCommandTable',dataList)
	$("#redisCommandTable").show()	
}

function show_stats(obj, inst){
	let dataList = requests('get','/api/db/redis/status/'+ obj["original"]["db_server"] +'/?type=stats')["data"]
	if ($('#redisStatsTable').hasClass('dataTable')) {
        dttable = $('#redisStatsTable').dataTable();
        dttable.fnClearTable();
        dttable.fnDestroy();         
	}	
	drewRedisStatusTables('redisStatsTable',dataList)
	$("#redisStatsTable").show()	
}
 