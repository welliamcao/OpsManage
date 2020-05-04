var sqlHistroyResults = {}
var sqlHistroyDataList = []

var statusLevelHtml = {
	    "high":'<span class="label label-danger">高</span>',
	    "mid":'<span class="label label-info">中</span>',
	    "low":'<span class="label label-success">低</span> '
	}

function InitSQLHistroyDataTable(tableId,url,buttons,columns,columnDefs){
	  sqlHistroyDataList = requests('get',url)
	  oOverviewTable =$('#'+tableId).dataTable(
			  {
				  	"dom": "Blfrtip",
				  	"buttons":buttons,
		    		"bScrollCollapse": false, 				
		    	    "bRetrieve": true,	
		    		"destroy": true, 
		    		"data":	sqlHistroyDataList['results'],
		    		"columns": columns,
		    		"columnDefs" :columnDefs,			  
		    		"language" : language,
		    		"lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
		    		"order": [[ 0, "ase" ]],
		    		"autoWidth": false	    			
		    	});
	  if (sqlHistroyDataList['next']){
		  $("button[name='page_next']").attr("disabled", false).val(sqlHistroyDataList['next']);	
	  }else{
		  $("button[name='page_next']").attr("disabled", true).val();
	  }
	  if (sqlHistroyDataList['previous']){
		  $("button[name='page_previous']").attr("disabled", false).val(sqlHistroyDataList['next']);	
	  }else{
		  $("button[name='page_previous']").attr("disabled", true).val();
	  }	    	 	  
}

function RefreshSQLHistroyDataTable(tableId, urlData){
	$.getJSON(urlData, null, function( dataList ){
    table = $('#'+tableId).dataTable();
    oSettings = table.fnSettings();
    
    table.fnClearTable(this);

    for (var i=0; i<dataList['results'].length; i++){
      table.oApi._fnAddData(oSettings, dataList['results'][i]);
      sqlHistroyResults[dataList["results"][i]["id"]] = dataList["results"][i]["exe_sql"]
    }

    oSettings.aiDisplay = oSettings.aiDisplayMaster.slice();
    table.fnDraw();
    
    if (dataList['next']){
  	  $("button[name='page_next']").attr("disabled", false).val(dataList['next']);	
    }else{
  	  $("button[name='page_next']").attr("disabled", true).val();
    }
    if (dataList['previous']){
  	  $("button[name='page_previous']").attr("disabled", false).val(dataList['previous']);	
    }else{
  	  $("button[name='page_previous']").attr("disabled", true).val();
    } 
            
  });	
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
				    "dom": "Blfrtip",
				    "buttons":buttons,				  
		    		"bScrollCollapse": false, 				
		    	    "bRetrieve": true,			
		    		"destroy": true, 
		    		"data":	dataList,
		    		"columns": columns,
		    		"columnDefs" :columnDefs,			  
		    		"language" : language,
		    		"iDisplayLength": 10,
		    		"lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
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


function makeDbQueryTableList(dataList){
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
	    	                           '<button type="button" name="btn-database-query" value="'+ row.id  +'" class="btn btn-default"  aria-label="Justify"><span class="fa fa-search-plus" aria-hidden="true"></span>' +	
	    	                           '</button>' +	
	    	                           '<button type="button" name="btn-database-table" value="'+ row.id +'" class="btn btn-default"  aria-label="Justify"><span class="fa fa-bar-chart" aria-hidden="true"></span>' +	
	    	                           '</button>' +  
	    	                           '<button type="button" name="btn-database-dict" value="'+ row.id + ':' + row.sid +'" class="btn btn-default"  aria-label="Justify"><span class="fa fa-cloud-download" aria-hidden="true"></span>' +	
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
	            "show_processlist":{  
	                "label":"当前进程",  
	                "icon": "fa fa-picture-o",
	                "action":function(data){
	                	var inst = $.jstree.reference(data.reference),
						obj = inst.get_node(data.reference);
	                	show_processlist(obj, inst)
	                }  
	            },	    		
	            "status":{  
	                "label":"数据库状态",  
	                "icon": "fa fa-bar-chart-o",
	                "action":function(data){
	                	var inst = $.jstree.reference(data.reference),
						obj = inst.get_node(data.reference);
	                	show_status(obj, inst)
	                }  
	            },
	            "innodb_status":{  
	                "label":"innodb状态",  
	                "icon": "fa fa-pie-chart",
	                "action":function(data){
	                	var inst = $.jstree.reference(data.reference),
						obj = inst.get_node(data.reference);
	                	show_innodb_status(obj, inst)
	                }  
	            },
	            "pxc":{  
	                "label":"pxc集群状态",  
	                "icon": "fa fa-line-chart",
	                "action":function(data){
	                	var inst = $.jstree.reference(data.reference),
						obj = inst.get_node(data.reference);
	                	show_pxc_status(obj, inst)
	                }  
	            },
	            "innodb_locked_trx":{  
	                "label":"innodb事务锁",  
	                "icon": "fa fa-area-chart",
	                "action":function(data){
	                	var inst = $.jstree.reference(data.reference),
						obj = inst.get_node(data.reference);
	                	show_innodb_locked_trx(obj, inst)
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
		            },	
		            "dump":{
	              		"separator_before"	: false,
						"separator_after"	: false,
						"_disabled"			: false, 
						"label"				: "导出表数据",
						"shortcut_label"	: 'F2',
						"icon"				: "fa fa-cloud-download",
						"action"			: function (data) {
							var inst = $.jstree.reference(data.reference),
							obj = inst.get_node(data.reference);
							dumpTabledata(obj)
						}
		            }	    
		    	}
		      }	    
	});		
}

function makeUserDBQueryHistory(db_id) {  	
    var columns = [
		            { "data": "id" },
		            { "data": "db_env"},
		            { "data": "db_host","className": "text-center" },
		            { "data": "db_name","className": "text-center"},
		            { "data": "exe_user","className": "text-center"},
		            { "data": "exe_sql"},	    		            
		            { "data": "exec_status","defaultContent": ''},
		            { "data": "exe_time","defaultContent": ''},
		            { "data": "exe_effect_row","defaultContent": ''},
		            { "data": "exe_result","defaultContent": ''},
		            { "data": "create_time"},   
	        ]
   var columnDefs = [  
					   	{
								targets: [0],
								render: function(data, type, row, meta) {
									if(row.favorite > 0){
										var favorite =  '<button type="button" name="btn-user-db-sql-favorite" value="' + row.id + ":" + row.favorite + ":" + row.exe_db +'" class="btn btn-default" title="取消收藏" aria-label="Justify"><span class="fa fa-heart" aria-hidden="true"></span></button>'
									}else{
										var favorite =  '<button type="button" name="btn-user-db-sql-favorite" value="' + row.id + ":" + row.favorite + ":" + row.exe_db +'" class="btn btn-default" title="收藏语句" aria-label="Justify"><span class="fa fa-heart-o" aria-hidden="true"></span></button>'
									}
									return '<div class="btn-group  btn-group-xs">' + favorite +	                
			    	                           '<button type="button" name="btn-user-db-sql-execute"  value="'+ row.id +'" class="btn btn-default" title="快速查询" aria-label="Justify"><span class="fa fa-search-plus" aria-hidden="true"></span>' +	
			    	                           '</button>' +			                            
		    	                           '</div>';									
								},
								"className": "text-center",
					     }, 	   
    		        	{
	   	    				targets: [1],
	   	    				render: function(data, type, row, meta) {
	   	                        if(row.db_env=="测试环境"){
	   	                        	return '<span class="label label-success">测试</span>'
	   	                        }else{
	   	                        	return '<span class="label label-danger">生产</span>'
	   	                        }
	   	    				},
	   	    				"className": "text-center",
		    		     },     		    		      		    		        		                 	    		     
    		        	{
	   	    				targets: [6],
	   	    				render: function(data, type, row, meta) {
	   	                        if(row.exec_status==0){
	   	                        	return '<span class="label label-success">成功</span>'
	   	                        }else{
	   	                        	return '<span class="label label-danger">失败</span>'
	   	                        }
	   	    				},
	   	    				"className": "text-center",
		    		     } 
	    		      ]	
    var buttons = []
    InitSQLHistroyDataTable("databaseSQLExecuteHistroy","/api/logs/sql/?exe_db="+db_id,buttons,columns,columnDefs)  
	if(sqlHistroyDataList["results"].length){
		for (var i = 0; i < sqlHistroyDataList["results"].length; ++i) {
			sqlHistroyResults[sqlHistroyDataList["results"][i]["id"]] = sqlHistroyDataList["results"][i]["exe_sql"]
		}
	}		    
}

function makeUserSQLSelect(ids,dataList){
	var binlogHtml = '<select required="required" class="selectpicker form-control" data-live-search="true"  data-size="10" data-width="100%" name="'+ ids +'" id="'+ids+'"  autocomplete="off" title="常用查询">'
	var selectHtml = '';
	for (var i=0; i <dataList.length; i++){
		selectHtml += '<option value="'+ dataList[i]["exe_sql"] +'">'+ dataList[i]["mark"] +'</option>' 					 
	};                        
	binlogHtml =  binlogHtml + selectHtml + '</select>';
	document.getElementById(ids).innerHTML= binlogHtml;							
	$('#'+ids).selectpicker('refresh');		
}

$(document).ready(function () {

	var randromChat = makeRandomId()
	
	try{
		var aceEditAdd = setAceEditMode("compile-editor-add","ace/mode/mysql","ace/theme/sqlserver");								 		  
	}
	catch(err){
		console.log(err)
	}		
	
    $("#db_user_sql").change(function(){ 
		let sql = $('#db_user_sql :selected').val()   
		if(sql.length){
	    	aceEditAdd.setValue("")
	    	aceEditAdd.insert(sql)			
		}
    }) 	
	
    if ($("#UserDatabaseListTable").length) {   

    	$('#UserDatabaseListTable tbody').on('click',"button[name='btn-database-query']",function(){   
        	let vIds = $(this).val();
        	let td = $(this).parent().parent().parent().find("td")
        	$("#dbChoice").html('<lable>数据库  <u class="red">'+ td.eq(1).text() +'</u> 查询入口<i class="fa fa-info-circle" data-toggle="tooltip" title="选择常用SQL"></i>:  </lable>')
			$("#db_query_btn").removeClass("disabled").text("查询").val(vIds)
    	    if ($('#databaseSQLExecuteHistroy').hasClass('dataTable')) {
    	    	dttable = $('#databaseSQLExecuteHistroy').dataTable();
    	    	dttable.fnClearTable();
    	    	dttable.fnDestroy(); 
    	    }					
			makeUserDBQueryHistory(vIds)
			$('#show_sql_result').show();	
			makeUserSQLSelect("db_user_sql",requests("get","/api/logs/sql/?exe_db="+vIds+"&&favorite=1")["results"])
        });	    	
    	
    	$('#UserDatabaseListTable tbody').on('click',"button[name='btn-database-table']",function(){   
        	let vIds = $(this).val();
        	let td = $(this).parent().parent().parent().find("td")
        	$("#dbTables").html('<i  class="fa  fa-paper-plane" >数据库  <u class="red">'+ td.eq(1).text() +'</u> 表结构</i>')
        	let dbname = td.eq(1).text()
        	var jsonData = {
                "did": vIds,
                "text": dbname,
                "icon": "fa fa-database",
                "children":[]
        	}
        	$.ajax({  
                cache: true,  
                type: "POST",  
                url:"/db/mysql/manage/", 
                data:{
                	"model": "table_list",
                	"db":vIds
                },
                async : false,  
	            error: function(response) {
	            	new PNotify({
	                    title: 'Ops Failed!',
	                    text: response.statusText,
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
		            	let respone = response["data"]		            	       	        	  
						for (var i=0; i <respone.length; i++){				    
							jsonData["children"].push({"db":vIds,"id":respone[i],"text":respone[i],"icon": "fa fa-bar-chart"})
	                        if (i>1000){
	                        	break
	                        }

						}
		            	drawTableTree("#dbTableTree",[jsonData])
		                $("#table-search-input").keyup(function () {
		                    var searchString = $(this).val();
		                    $('#dbTableTree').jstree('search', searchString);
		                });			            	
					}	
	            	
	            } 
        	});          	
        });	    	
    	
    	$('#UserDatabaseListTable tbody').on('click',"button[name='btn-database-dict']",function(){   
        	let vIds = $(this).val().split(":");
        	let td = $(this).parent().parent().parent().find("td")
        	downLoadFile({ //调用下载方法
	        	url:"/api/db/mysql/server/"+vIds[1]+"/db/"+vIds[0]+"/dict/"
	        });          	
        });	   
    	   		
    }	
	
	drawTree('#dbTree',"/api/db/mysql/tree/?db_rw=r/w&db_rw=read")
	
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
					  url: '/api/db/mysql/user/list/?db_server='+select_node["db_server"],
				      success:function(response){	
				    	  if ($('#UserDatabaseListTable').hasClass('dataTable')) {
				            dttable = $('#UserDatabaseListTable').dataTable();
				            dttable.fnClearTable();
				            dttable.fnDestroy(); 
				    	  }			    	  
				    	  makeDbQueryTableList(response)
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

    $("#db_query_btn").on('click', function () {
        let btnObj = $(this);
        btnObj.attr('disabled', true);
        let db = $(this).val()
        if (db > 0) {
            $('#show_sql_result').show();
            let sql = aceEditAdd.getSession().getValue();
            if (sql.length == 0 || db == 0) {
                new PNotify({
                    title: 'Warning!',
                    text: 'SQL内容与数据库不能为空',
                    type: 'warning',
                    styling: 'bootstrap3'
                });
                btnObj.removeAttr('disabled');
                return false;
            }
            //删除最后一个;符号
            while (sql[sql.length - 1] === ';')
               sql = sql.substr(0, sql.length - 1);   
 
            //SQL过滤
            let sql_list = sql.split(/\n/)
            for (let i = 0; i < sql_list.length; i++) {
            	//以#开头的SQL就替换掉
            	if(/^#/.test(sql_list[i])){
            		sql = sql.replace(sql_list[i],'');
            	}
            	//删除sql两边的空格字符串
            	sql = sql.replace(/^\s*|\s*$/g,"");
            }
          
            if (sql.split(";").length > 10) {
                new PNotify({
                    title: 'Warning!',
                    text: '查询最多支持10条query',
                    type: 'warning',
                    styling: 'bootstrap3'
                });
                btnObj.removeAttr('disabled');
                return false;
            }
            $.ajax({
                url: '/db/mysql/manage/',
                type: "POST",
                "dateType": "json",
                data: {
                    "db": db,
                    "model": 'query_sql',
                    "sql": sql
                },  //提交参数
                success: function (response) {
                    btnObj.removeAttr('disabled');
                    let ulTags = '<ul class="list-unstyled timeline widget">';
                    let tableHtml = '';
                    let liTags = '';
                    let tablesList = [];
                    if (response['code'] == "200" && response["data"].length > 0) {
                        for (let i = 0; i < response["data"].length; i++) {
                            let tableId = "query_result_list_" + i;
                            tablesList.push(tableId);
                            let table_i_html = '';
                            if (response["data"][i]["dataList"] instanceof Array) {
                                table_i_html = '<table class="table" id="' + tableId + '"><thead><tr>';
                                let trHtml = '';
                                for (let x = 0; x < response["data"][i]["dataList"][2].length; x++) {
                                    trHtml = trHtml + '<th>' + response["data"][i]["dataList"][2][x] + '</th>';
                                }
                                table_i_html = table_i_html + trHtml + '</tr></thead><tbody>';
                                let trsHtml = '';
                                for (let y = 0; y < response["data"][i]["dataList"][1].length; y++) {
                                    let tdHtml = '<tr>';
                                    for (let z = 0; z < response["data"][i]["dataList"][1][y].length; z++) {
                                        tdHtml = tdHtml + '<td>' + response["data"][i]["dataList"][1][y][z] + '</td>';
                                    }
                                    trsHtml = trsHtml + tdHtml + '</tr>';
                                }
                                table_i_html += trsHtml + '</tbody></table>'
                            } else {
                                table_i_html = '<div style="margin-bottom: 20px;margin-left: 20px;">' + response["data"][i]["msg"] + '<div/>'
                            }
                            tableHtml = tableHtml + '<fieldset><legend style="margin-bottom: 10px;"> SQL： <code>' + response["data"][i]['sql'] + '</code> <span class="pull-right">耗时：'+ response["data"][i]['time'] +'</span></legend>'  + table_i_html + '</fieldset>';
                        }
                        $("#query_result").html(tableHtml);
                        if (tablesList.length) {
                            for (var i = 0; i < tablesList.length; i++) {
                                var table = $("#" + tablesList[i]).DataTable({
                                    dom: 'Bfrtip',
                                    "lengthMenu": [[50, 150, 450, -1], [50, 150, 450, "All"]],
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
                                    language: {
                                        "sProcessing": "处理中...",
                                        "sLengthMenu": "显示 _MENU_ 项结果",
                                        "sZeroRecords": "没有匹配结果",
                                        "sInfo": "显示第 _START_ 至 _END_ 项结果，共 _TOTAL_ 项",
                                        "sInfoEmpty": "显示第 0 至 0 项结果，共 0 项",
                                        "sInfoFiltered": "(由 _MAX_ 项结果过滤)",
                                        "sInfoPostFix": "",
                                        "sSearch": "搜索:",
                                        "sUrl": "",
                                        "sEmptyTable": "表中数据为空",
                                        "sLoadingRecords": "载入中...",
                                        "sInfoThousands": ",",
                                        "oPaginate": {
                                            "sFirst": "首页",
                                            "sPrevious": "上页",
                                            "sNext": "下页",
                                            "sLast": "末页"
                                        },
                                        "oAria": {
                                            "sSortAscending": ": 以升序排列此列",
                                            "sSortDescending": ": 以降序排列此列"
                                        }
                                    },
                                });
                            }
                        }
                        RefreshSQLHistroyDataTable('databaseSQLExecuteHistroy','/api/logs/sql/?exe_db='+db)
                    } else {
                        var selectHtml = '<div id="query_result">' + response["msg"] + '</div>';
                        $("#query_result").html(selectHtml);
                    }
                },
                error: function (response) {
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
    	
	$('#databaseSQLExecuteHistroy tbody').on('click',"button[name='btn-user-db-sql-execute']",function(){   
    	let vIds = $(this).val();
    	let td = $(this).parent().parent().parent().find("td")
    	aceEditAdd.setValue("")
    	aceEditAdd.insert(td.eq(5).text())
    });		
	
	$('#databaseSQLExecuteHistroy tbody').on('click',"button[name='btn-user-db-sql-favorite']",function(){   
    	let vIds = $(this).val().split(":");
    	let td = $(this).parent().parent().parent().find("td")
    	let sql = td.eq(5).text()
    	if (vIds[1] > 0){
    		$.confirm({
    		    title: '取消收藏',
    		    content:  '确认取消收藏这条SQL吗？',
    		    type: 'red',
    		    buttons: {
    		       确定: function () {
    		    	$.ajax({  
    		            cache: true,  
			            type: "put",  
			            url:"/api/logs/sql/" + vIds[0] + '/',  
			            data:{
			            	"favorite":0,
			            	"mark":""
			            },
    		            error: function(response) {  
    		            	new PNotify({
    		                    title: 'Ops Failed!',
    		                    text: "操作失败",
    		                    type: 'error',
    		                    styling: 'bootstrap3'
    		                });     
    		            },  
    		            success: function(response) {  
    		            	new PNotify({
    		                    title: 'Success!',
    		                    text: "操作成功",
    		                    type: 'success',
    		                    styling: 'bootstrap3'
    		                });	 
    		            	makeUserSQLSelect("db_user_sql",requests("get","/api/logs/sql/?exe_db="+vIds[2]+"&&favorite=1")["results"])
    		            	RefreshSQLHistroyDataTable('databaseSQLExecuteHistroy','/api/logs/sql/?exe_db='+vIds[2])
    		            }  
    		    	});
    		        },
    		        取消: function () {
    		            return true;			            
    		        },			        
    		    }
    		});	    		
    		
    	}else{
    	    $.confirm({
    	        icon: 'fa fa-plus',
    	        type: 'blue',
    	        title: '收藏SQL语句',
    	        content: '<form  data-parsley-validate class="form-horizontal form-label-left">' +
    			          '<div class="form-group">' +
    			            '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">名称: <span class="required">*</span>' +
    			            '</label>' +
    			            '<div class="col-md-6 col-sm-6 col-xs-12">' +
    			              '<input type="text"  name="mark" value="" required="required" class="form-control col-md-7 col-xs-12">' +
    			            '</div>' +
    			          '</div>' +		          
    			        '</form>',
    	        buttons: {
    	            '取消': function() {},
    	            '保存': {
    	                btnClass: 'btn-blue',
    	                action: function() {
    	                	var formData = {};	
    	            		var vipForm = this.$content.find('input');                	
    	            		for (var i = 0; i < vipForm.length; ++i) {
    	            			var name =  vipForm[i].name
    	            			var value = vipForm[i].value 
    	            			if (name.length >0 && value.length > 0){
    	            				formData[name] = value	
    	            			};		            						
    	            		};	
    	            		formData["favorite"] = 1
    				    	$.ajax({  
    				            cache: true,  
    				            type: "put",  
    				            url:"/api/logs/sql/" + vIds[0] + '/', 
    				            data:formData,
    				            error: function(request) {  
    				            	new PNotify({
    				                    title: 'Ops Failed!',
    				                    text: request.responseText,
    				                    type: 'error',
    				                    styling: 'bootstrap3'
    				                });       
    				            },  
    				            success: function(data) {  
    				            	new PNotify({
    				                    title: 'Success!',
    				                    text: 'SQL收藏成功',
    				                    type: 'success',
    				                    styling: 'bootstrap3'
    				                }); 
    				            	makeUserSQLSelect("db_user_sql",requests("get","/api/logs/sql/?exe_db="+vIds[2]+"&&favorite=1")["results"])
    				            	RefreshSQLHistroyDataTable('databaseSQLExecuteHistroy','/api/logs/sql/?exe_db='+vIds[2])
    				            }  
    				    	});
    	                }
    	            }
    	        }
    	    });    		
    	}
	    	
    });	
	    
})    

function dumpTabledata(obj){
	if (obj["original"]["db"]){
        $.confirm({
            icon: 'fa fa-edit',
            type: 'blue',
            title: `导出表${obj.id}数据`,
            height: 'auto',
            content: '' +
                '<div class="form-group">' +
                '<label>任务名称：</label>' +
                '<input type="text" placeholder="任务名称" class="form-control" name="task_name" value="'+ `导出表${obj.id}数据 ` +'" required />' +                
                '<label>where：</label>' +
                '<input type="text" placeholder="`name`=\'1\' AND `id`>10 #不填就导出全表数据" class="form-control" name="where"/>' +
                '<label>邮箱：</label>' +
                '<input type="text" placeholder="303350019@qq.com #不填默认发给自己" class="form-control" name="email"/>' +                
                '</div>',
            buttons: {
                "导出": {
                    btnClass: 'btn-blue',
                    action: function () {
                    	let email = this.$content.find('[name=email]').val().trim();
                        let task_name = this.$content.find('[name=task_name]').val().trim();
                        if (!task_name) {
                            $.alert("<label>任务名称不能为空</label>")
                            return false
                        }   
                        let pattern = /^([A-Za-z0-9_\-.])+@([A-Za-z0-9_\-.])+\.([A-Za-z]{2,4})$/;
                        if (!pattern.test(email) && email.length > 0) {
                            $.alert("<label>请输入正确的邮箱地址</label>");
                            return false
                        }                        
                        let where = this.$content.find('[name=where]').val().trim();
                        $.ajax({
                            url: "/db/mysql/manage/",
                            type: "POST",
                            data: {
                            	db: obj["original"]["db"],
                            	table_name: obj["original"]["id"],
                                model: "dump_table",
                                where: where,
                                email: email,
                                task_name: task_name,
                            },
                            success: function (response) {
                                if (response["code"] != 200) {
                                    new PNotify({
                                        title: 'Ops Failed!',
                                        text: response["msg"],
                                        type: 'error',
                                        styling: 'bootstrap3'
                                    });
                                } else {
                                    new PNotify({
                                        title: 'Success!',
                                        text: "导出任务提交成功",
                                        type: 'success',
                                        styling: 'bootstrap3'
                                    });
                                }
                            },
                            error: function (response) {
                                new PNotify({
                                    title: 'Ops Failed!',
                                    text: response.responseText,
                                    type: 'error',
                                    styling: 'bootstrap3'
                                });
                            }
                        })

                    },
                },
                cancel: function () {
                    //close
                },
            },
            onContentReady: function () {
                // bind to events
                var jc = this;
                this.$content.find('form').on('submit', function (e) {
                    // if the user submits the form by pressing enter in the field.
                    e.preventDefault();
                });
            }
        });		
	}
}

function viewTableSchema(obj){
	if (obj["original"]["db"]){
    	$.ajax({  
            cache: true,  
            type: "POST",    
            async: false,
            url:"/db/mysql/manage/",
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
function drewMysqlStatusTables(ids, dataList){
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

function show_status(obj,inst){
	let dataList = requests('get','/api/db/mysql/status/'+ obj["original"]["db_server"] +'/?type=status')["data"]
	if ($('#mysqlStatusTable').hasClass('dataTable')) {
        dttable = $('#mysqlStatusTable').dataTable();
        dttable.fnClearTable();
        dttable.fnDestroy();         
	}	
	drewMysqlStatusTables('mysqlStatusTable',dataList)
	$("#mysqlStatusTable").show()
}

function show_innodb_status(obj,inst){
	let dataList = requests('get','/api/db/mysql/status/'+ obj["original"]["db_server"] +'/?type=innodb_status')["data"]
	if ($('#mysqlInnodbStatusTable').hasClass('dataTable')) {
        dttable = $('#mysqlInnodbStatusTable').dataTable();
        dttable.fnClearTable();
        dttable.fnDestroy();         
	}	
	drewMysqlStatusTables('mysqlInnodbStatusTable',dataList)
	$("#mysqlInnodbStatusTable").show()
}

function show_pxc_status(obj,inst){
	let dataList = requests('get','/api/db/mysql/status/'+ obj["original"]["db_server"] +'/?type=pxc_status')["data"]
	if ($('#mysqlPxcTable').hasClass('dataTable')) {
        dttable = $('#mysqlPxcTable').dataTable();
        dttable.fnClearTable();
        dttable.fnDestroy();         
	}	
	drewMysqlStatusTables('mysqlPxcTable',dataList)
	$("#mysqlPxcTable").show()
}

function show_innodb_locked_trx(obj,inst){
	let response = requests('get','/api/db/mysql/status/'+ obj["original"]["db_server"] +'/?type=innodb_locked_trx')
	if ($('#mysqlInnodbTrxStatusTable').hasClass('dataTable')) {
        dttable = $('#mysqlInnodbTrxStatusTable').dataTable();
        dttable.fnClearTable();
        dttable.fnDestroy();         
	}	
	var tableHtml = ''
	if (response['code'] == "200" && response["data"].length > 0){
		if (response["data"][0] >= 0){
			var tableHtml = '<table class="table" id="mysqlInnodbTrxStatusTable"><caption>Innodb锁等待</caption><thead><tr>'
			var trHtml = '';
			for (var x=0; x <response["data"][2].length; x++){
				trHtml = trHtml + '<th>' + response["data"][2][x] +'</th>';
			}; 	
			tableHtml = tableHtml + trHtml + '</tr></thead><tbody>';
			var trsHtml = '';
			for (var y=0; y <response["data"][1].length; y++){
				var tdHtml = '<tr>';
				for (var z=0; z < response["data"][1][y].length; z++){
					tdHtml = tdHtml + '<td>' + response["data"][1][y][z] +'</td>';
				} 	
				trsHtml = trsHtml + tdHtml + '</tr>';
			}                    	
			tableHtml = tableHtml + trsHtml +  '</tbody></table>';														
		}			
		$("#mysqlInnodbTrxStatusTable").html(tableHtml);
		var table = $("#mysqlInnodbTrxStatusTable").DataTable( {
	        dom: 'Blfrtip',
	        "pageLength": 100,
	        buttons: [],
			language : language				            
		});	
						
	}		
	$("#mysqlInnodbTrxStatusTable").show()
}

function show_processlist(obj,inst){
	let response = requests('get','/api/db/mysql/status/'+ obj["original"]["db_server"] +'/?type=processlist')
	if ($('#mysqlProcesslistTable').hasClass('dataTable')) {
        dttable = $('#mysqlProcesslistTable').dataTable();
        dttable.fnClearTable();
        dttable.fnDestroy();         
	}	
	var tableHtml = ''	
	if (response['code'] == "200" && response["data"].length > 0){
		if (response["data"][0] >= 0){
			var tableHtml = '<table class="table" id="mysqlProcesslistTable"><caption>MySQL当前进程</caption><thead><tr>'
			var trHtml = '';
			for (var x=0; x <response["data"][2].length; x++){
				trHtml = trHtml + '<th>' + response["data"][2][x] +'</th>';
			}; 	
			tableHtml = tableHtml + trHtml + '</tr></thead><tbody>';
			var trsHtml = '';
			for (var y=0; y <response["data"][1].length; y++){
				var tdHtml = '<tr>';
				for (var z=0; z < response["data"][1][y].length; z++){
					tdHtml = tdHtml + '<td>' + response["data"][1][y][z] +'</td>';
				} 	
				trsHtml = trsHtml + tdHtml + '</tr>';
			}                    	
			tableHtml = tableHtml + trsHtml +  '</tbody></table>';														
		}			
		$("#mysqlProcesslistTable").html(tableHtml);
		var table = $("#mysqlProcesslistTable").DataTable( {
	        dom: 'Blfrtip',
	        "pageLength": 100,
	        buttons: [],
			language : language				            
		});	
						
	}		
	$("#mysqlProcesslistTable").show()	
}
 