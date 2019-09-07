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
	    	                           '<button type="button" name="btn-database-query" value="'+ row.id +'" class="btn btn-default"  aria-label="Justify"><span class="glyphicon glyphicon glyphicon-zoom-in" aria-hidden="true"></span>' +	
	    	                           '</button>' +	
	    	                           '<button type="button" name="btn-database-table" value="'+ row.id +'" class="btn btn-default"  aria-label="Justify"><span class="fa fa-bar-chart" aria-hidden="true"></span>' +	
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

	try{
		var aceEditAdd = setAceEditMode("compile-editor-add","ace/mode/mysql","ace/theme/sqlserver");								 		  
	}
	catch(err){
		console.log(err)
	}		
	
	
    if ($("#UserDatabaseListTable").length) {   

    	$('#UserDatabaseListTable tbody').on('click',"button[name='btn-database-query']",function(){   
        	let vIds = $(this).val();
        	let td = $(this).parent().parent().parent().find("td")
        	$("#dbChoice").html('<i  class="fa  fa-paper-plane" >数据库  <u class="red">'+ td.eq(1).text() +'</u> 查询入口</i>')
			$("#db_query_btn").removeClass("disabled").text("查询").val(vIds)
        });	    	
    	
    	$('#UserDatabaseListTable tbody').on('click',"button[name='btn-database-table']",function(){   
        	let vIds = $(this).val();
        	let td = $(this).parent().parent().parent().find("td")
        	$("#dbTables").html('<i  class="fa  fa-paper-plane" >数据库  <u class="red">'+ td.eq(1).text() +'</u> 表结构</i>')
        	let dbname = td.eq(1).text()
        	var jsonData = {
                "id": 1,
                "text": dbname,
                "icon": "fa fa-database",
                "children":[]
        	}
        	$.ajax({  
                cache: true,  
                type: "POST",  
                url:"/db/manage/", 
                data:{
                	"model": "table_list",
                	"db":vIds
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
    	
    }	
	
	drawTree('#dbTree',"/api/db/tree/?db_rw=r/w&db_rw=read")
	
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
					  url: '/api/db/user/list/?db_server='+select_node["db_server"],
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
    
	$("#db_query_btn").on('click', function() {
		var btnObj = $(this);
		btnObj.attr('disabled',true); 
		var db = $(this).val()
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


function viewTableSchema(obj){
	if (obj["original"]["db"]){
    	$.ajax({  
            cache: true,  
            type: "POST",    
            async: false,
            url:"/db/manage/",
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
 