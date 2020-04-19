var orderMode = {
	    "0":'邮箱',
	    "1":'微信',         
	    "2":'钉钉',		
	}

var orderAuditStatusHtml = {
	    "1":'<span class="label label-danger">已拒绝</span>',
	    "2":'<span class="label label-info">审核中</span>',
	    "3":'<span class="label label-success">已授权</span> '
	}

var orderExecuteStatusHtml = {
		"0":'<span class="label label-warning">已提交</span>',
	    "1":'<span class="label label-info">处理中</span>',
	    "2":'<span class="label label-success">已完成</span>',
	    "3":'<span class="label label-warning">已回滚</span> ',
	    "4":'<span class="label label-default">已关闭</span> ',
	    "5":'<span class="label label-danger">执行失败</span> ',
	}

var orderTypeHtml = {
	"0":'<b>SQL更新</b>',
	"1":'<b>运维服务</b>',
	"2":'<b>文件分发</b>',
	"3":'<b>文件下载</b>'
}

var orderTypeJson = {
	"0":'sql',
	"1":'service',
	"2":'fileupload',
	"3":'filedownload'		
}

var orderSQLtypeJson = {
	"online":"工具审核",
	"file":"SQL文件",
	"human":"人工审核",
	"service":"运维服务"
}

var dbEnvHtml = {
	"beta":'<span class="label label-success">测试环境</span>',	
	"ga":'<span class="label label-danger">生产环境</span>',	
}

var orderBackupHmtl = {
	"0":'<span class="label label-warning">无备份</span>',	
	"1":'<span class="label label-success">有备份</span>',
}


var userInfo = {
		
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

function get_url_param(name) {
	 var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
	 var r = window.location.search.substr(1).match(reg);
	 if (r != null) return unescape(r[2]); return null; 
}

function AssetsSelect(name,dataList,selectIds){
    var selectIdsList = [];
	if(selectIds) {
	    selectIdsList = JSON.parse(selectIds);
	}
	switch(name)
	   {
		   case "project":
			   action = 'onchange="javascript:oBtProjectSelect(this);"'
		       break;			       
		   default:
			   action = ''	       
	   }
	var binlogHtml = '<select required="required" class="selectpicker form-control" data-live-search="true"  data-size="10" data-width="100%" '+ action +' name="'+ name +'"autocomplete="off"><option value="">选择一个进行操作</option>'
	var selectHtml = '';
	for (var i=0; i <dataList.length; i++){
		if(dataList[i][name+"_name"]){
			var text = dataList[i][name+"_name"]
			selectHtml += '<option value="'+ dataList[i]["id"] +'">'+text +'</option>'
		}else{
			switch(name)
			{
			case "custom":
				var text = dataList[i]["detail"]["ip"]
				var count = 0
                for (var j=0; j <selectIdsList.length; j++){
					if(selectIdsList[j]==dataList[i]["id"]){
						count = count + 1				
					}
				}
				if (count > 0){
					selectHtml += '<option selected="selected" value="'+ dataList[i]["id"] +'">'+text +'</option>' 	
				}				
				break;
			case "files":
				var text =  dataList[i]["file_path"]
				selectHtml += '<option selected="selected" value="'+ dataList[i]["id"] +'">'+text +'</option>'
				break;
			default:
				var text = dataList[i]["name"]
				selectHtml += '<option value="'+ dataList[i]["id"] +'">'+text +'</option>'
				break;
			}				
		}					 
	};                        
	binlogHtml =  binlogHtml + selectHtml + '</select>';
	$("select[name='"+name+"']").html(binlogHtml)
	$("select[name='"+name+"']").selectpicker('refresh');		
}

function makeOrderAuditStatusSelect(value){
    switch(value)
    {
    case 1:
    	return '<select class="form-control" name="order_audit_status">' + 
	                  '<option selected="selected"  value="1">拒绝</option>' +
	                  '<option value="2">审核</option>' +
	                  '<option value="3">通过</option>' +
               '</select>'  
    case 2:
    	return '<select class="form-control" name="order_audit_status">' + 
	                '<option value="1">拒绝</option>' +
	                '<option selected="selected" value="2">审核</option>' +
	                '<option value="3">通过</option>' +
               '</select>' 
    case 3:
    	return '<select class="form-control" name="order_audit_status">' + 
	                '<option value="1">拒绝</option>' +
	                '<option value="2">审核</option>' +
	                '<option selected="selected" value="3">通过</option>' +
               '</select>'
    }

}

function makeOrderExecuteStatusSelect(value){
    switch(value)
    {
    case 0:
    	return '<select class="form-control" name="order_execute_status">' + 
                  '<option selected="selected" value="0">已提交</option>' +
                  '<option value="1">处理中</option>' +
                  '<option value="2">已完成</option>' +
                  '<option value="3">已回滚</option>' +
                  '<option value="4">已关闭</option>' +
                  '<option value="5">执行失败</option>' +
               '</select>'      
    case 1:
    	return '<select class="form-control" name="order_execute_status">' + 
		        '<option value="0">已提交</option>' +
		        '<option selected="selected" value="1">处理中</option>' +
		        '<option value="2">已完成</option>' +
		        '<option value="3">已回滚</option>' +
		        '<option value="4">已关闭</option>' +
		        '<option value="5">执行失败</option>' +
		     '</select>' 
    case 2:
    	return '<select class="form-control" name="order_execute_status">' + 
		        '<option selected="selected"  value="0">已提交</option>' +
		        '<option value="1">处理中</option>' +
		        '<option selected="selected" value="2">已完成</option>' +
		        '<option value="3">已回滚</option>' +
		        '<option value="4">已关闭</option>' +
		        '<option value="5">执行失败</option>' +
		     '</select>' 
    case 3:
    	return '<select class="form-control" name="order_execute_status">' + 
		        '<option value="0">已提交</option>' +
		        '<option value="1">处理中</option>' +
		        '<option value="2">已完成</option>' +
		        '<option selected="selected" value="3">已回滚</option>' +
		        '<option value="4">已关闭</option>' +
		        '<option value="5">执行失败</option>' +
		     '</select>' 
    case 4:
    	return '<select class="form-control" name="order_execute_status">' + 
		        '<option selected="selected"  value="0">已提交</option>' +
		        '<option value="1">处理中</option>' +
		        '<option value="2">已完成</option>' +
		        '<option value="3">已回滚</option>' +
		        '<option selected="selected" value="4">已关闭</option>' +
		        '<option value="5">执行失败</option>' +
		     '</select>'  
    case 5:
    	return '<select class="form-control" name="order_execute_status">' + 
		        '<option selected="selected"  value="0">已提交</option>' +
		        '<option value="1">处理中</option>' +
		        '<option value="2">已完成</option>' +
		        '<option value="3">已回滚</option>' +
		        '<option value="4">已关闭</option>' +
		        '<option selected="selected" value="5">执行失败</option>' +
		     '</select>'		        
    }

}


/*function DynamicSelect(ids,value){
	$("#" + ids +" option").each(function(){ 
		$(this).prop("selected",false);   
	})
	$("#" + ids +" option[value='" + value +"']").prop("selected",true);	
}*/

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


function DynamicSelect(ids,value){
	$("#" + ids +" option").each(function(){ 
		$(this).prop("selected",false);   
	})
	$("#" + ids +" option[value='" + value +"']").prop("selected",true);	
	$("#" + ids).attr("disabled","")
	$('#'+ids).selectpicker('refresh');	
}

function makeUserSelect(ids,dataList){
	var binlogHtml = '<select required="required" class="selectpicker form-control" data-live-search="true"  data-size="10" data-width="100%" name="'+ ids +'" id="'+ids+'"  autocomplete="off">'
	var selectHtml = '';
	for (var i=0; i <dataList.length; i++){
		selectHtml += '<option value="'+ dataList[i]["id"] +'">'+ dataList[i]["name"] +'</option>' 					 
	};                        
	binlogHtml =  binlogHtml + selectHtml + '</select>';
	$('#'+ids).html(binlogHtml)		
	$('#'+ids).selectpicker('refresh');		
}

function InitDataTable(tableId, url, buttons, columns, columnDefs, page){
	  var data = requests('get',url)
	  oOverviewTable =$('#'+tableId).dataTable({
				    "dom": "Blfrtip",
				    "buttons":buttons,
		    		"bScrollCollapse": false, 				
		    	    "bRetrieve": true,			
		    		"destroy": true, 
		    		"data":	data["results"],
		    		"columns": columns,
		    		"columnDefs" :columnDefs,			  
		    		"language" : language,
		    		"lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
		    		"order": [[ 0, "ase" ]],
		    		"autoWidth": false	    			
	  });
	  if (data['next']){
		  $("button[name='"+ page +"_page_next']").attr("disabled", false).val(data['next']);	
	  }else{
		  $("button[name='"+ page +"_page_next']").attr("disabled", true).val();
	  }
	  if (data['previous']){
		  $("button[name='"+ page +"_page_previous']").attr("disabled", false).val(data['next']);	
	  }else{
		  $("button[name='"+ page +"_page_previous']").attr("disabled", true).val();
	  }	  

}

function RefreshTable(tableId, urlData, page){
	$.getJSON(urlData, null, function( dataList )
	{
	  table = $('#'+tableId).dataTable();
	  oSettings = table.fnSettings();
	  
	  table.fnClearTable(this);
	
	  for (var i=0; i<dataList["results"].length; i++)
	  {
	    table.oApi._fnAddData(oSettings, dataList["results"][i]);
	  }
	
	  oSettings.aiDisplay = oSettings.aiDisplayMaster.slice();
	  table.fnDraw();
	  if (dataList['next']){
	   	  $("button[name='"+ page +"_page_next']").attr("disabled", false).val(dataList['next']);	
	  }else{
	   	  $("button[name='"+ page +"_page_next']").attr("disabled", true).val();
	  }
	  if (dataList['previous']){
	   	  $("button[name='"+ page +"_page_previous']").attr("disabled", false).val(dataList['previous']);	
	  }else{
	   	  $("button[name='"+ page +"_page_previous']").attr("disabled", true).val();
	  } 	  
	});
}


function orderInfoFormat(dataList) {
	
	switch(dataList["order_type"])
	{
	case 0:
		if(dataList["detail"]["order_err"]){
			var err = '<td class="col-md-1 col-sm-12 col-xs-12"><a data-toggle="modal" id="tooltips-err-'+dataList["id"]+'">'+dataList["detail"]["order_err"].substring(-1,10)+'...</a></td>'
		}else{
			var err = '<td class="col-md-1 col-sm-12 col-xs-12">无</td>'
		}
		var sqlHtml = '<div class="col-md-6 col-sm-12 col-xs-12">' +
			    			'<legend>工单明细</legend>' +
			    				'<table class="table" cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">'+ 
			    				'<tr>' +
			    					'<th>SQL类型</th>' +
			    					'<th>SQL内容</th>' +
			    					'<th>错误信息</th>' +
			    					'<th>是否备份</th>' +
			    					'<th>取消原因</th>' +
			    				'</tr>' + 
			    				'</tr>' + 
									 '<td class="col-md-1 col-sm-12 col-xs-12"><code>'+ orderSQLtypeJson[dataList["detail"]["order_type"]] +'</code></td>'+ 
								  	 '<td class="col-md-1 col-sm-12 col-xs-12"><a data-toggle="modal" id="tooltips-sql-'+dataList["id"]+'">'+dataList["detail"]["order_sql"].substring(-1,10)+'...</a></td>' +
								  	  err +
								  	 '<td class="col-md-1 col-sm-12 col-xs-12">'+ orderBackupHmtl[dataList["detail"]["sql_backup"]] +'</td>' +
								  	 '<td class="col-md-1 col-sm-12 col-xs-12">'+ dataList["order_mark"] +'</td>' +
							  	 '</tr>' +		    				
			    				'</table>' +
		    				'</div>'; 	
			
	    var dbHtml = '<div class="col-md-6 col-sm-12 col-xs-12">' +
		    				'<legend>目标数据库</legend>' +
		    				'<table class="table" cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">'+
			    				'<tr>' +
			    					'<th>环境</th>' +
			    					'<th>数据库</th>' +
			    					'<th>数据库地址</th>' +
			    					'<th>端口</th>' +
		    					'</tr>'	+    				
			    				'</tr>' + 
									 '<td class="col-md-1 col-sm-12 col-xs-12">'+ dataList["detail"]["db"]["db_env"] +'</td>'+ 
								  	 '<td class="col-md-1 col-sm-12 col-xs-12">'+ dataList["detail"]["db"]["db_name"] +'</td>' +
								  	 '<td class="col-md-1 col-sm-12 col-xs-12">'+ dataList["detail"]["db"]["ip"] +'</td>' +
								  	 '<td class="col-md-1 col-sm-12 col-xs-12">'+ dataList["detail"]["db"]["db_port"] +'</td>' +
							  	 '</tr>' +
		    				'</table>' +
	    				'</div>'; 
	    return '<div class="row">'+ sqlHtml + '</div><div class="row">' +  dbHtml + '</div>';
	case 2:
	    var trHtml = '';
		for (var i=0; i <dataList["detail"]["files"].length; i++){	
		    trHtml += '<tr><td class="col-md-1 col-sm-12 col-xs-12">'+ dataList["detail"]["files"][i]["file_path"] +'</td>'+ '<td class="col-md-1 col-sm-12 col-xs-12">'+ dataList["detail"]["files"][i]["file_type"] +'</td></tr>'	    
		};
		var uploadHtml = '<div class="col-md-6 col-sm-12 col-xs-12">' +
			    			'<legend>工单明细</legend>' +
			    				'<table class="table table-striped" cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">'+ 
			    				'<tr>' +
			    					'<th>目标路径</th>' +
			    					'<th>工单内容</th>' +
			    					'<th>目标服务器</th>' +
			    					'<th>宿主</th>' +
			    					'<th>权限</th>' +
			    					'<th>取消原因</th>' +
			    				'</tr>' + 
			    				'</tr>' + 
									 '<td class="col-md-1 col-sm-12 col-xs-12">'+ dataList["detail"]["dest_path"] +'</td>'+ 
								  	 '<td class="col-md-1 col-sm-12 col-xs-12"><a data-toggle="modal" id="tooltips-order_content-'+dataList["id"]+'">'+dataList["detail"]["order_content"].substring(-1,10)+'...</a></td>' +
								  	 '<td class="col-md-1 col-sm-12 col-xs-12"><a data-toggle="modal" id="tooltips-order_server-' +dataList["id"]+'">'+dataList["detail"]["server"][0].substring(-1,10)+'...</a></td>' +
								  	 '<td class="col-md-1 col-sm-12 col-xs-12">'+ dataList["detail"]["chown_user"] +'</td>' +
								  	 '<td class="col-md-1 col-sm-12 col-xs-12">'+ dataList["detail"]["chown_rwx"] +'</td>' +
								  	'<td class="col-md-1 col-sm-12 col-xs-12">'+ dataList["order_mark"] +'</td>' +
							  	 '</tr>' +		    				
			    				'</table>' +
		    				'</div>'; 	
			
	    var fileHtml = '<div class="col-md-6 col-sm-12 col-xs-12">' +
		    				'<legend>文件信息</legend>' +
		    				'<table class="table table-striped" cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">'+
			    				'<tr>' +
			    					'<th>文件名称</th>' +
			    					'<th>文件类型(检测)</th>' +
		    					'</tr>'	+    				
			    				 trHtml  +
		    				'</table>' +
	    				'</div>'; 	
	    return '<div class="row">'+ uploadHtml + '</div><div class="row">' +  fileHtml + '</div>';
	    
	case 3:
		var downloadHtml = '<div class="col-md-6 col-sm-12 col-xs-12">' +
		'<legend>工单明细</legend>' +
			'<table class="table table-striped" cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">'+ 
			'<tr>' +
				'<th>目标路径</th>' +
				'<th>工单内容</th>' +
				'<th>目标服务器</th>' +
				'<th>取消原因</th>' +
			'</tr>' + 
			'</tr>' + 
				 '<td class="col-md-1 col-sm-12 col-xs-12">'+ dataList["detail"]["dest_path"] +'</td>'+ 
			  	 '<td class="col-md-1 col-sm-12 col-xs-12"><a data-toggle="modal" id="tooltips-order_content-'+dataList["id"]+'">'+dataList["detail"]["order_content"].substring(-1,10)+'...</a></td>' +
			  	 '<td class="col-md-1 col-sm-12 col-xs-12"><a data-toggle="modal" id="tooltips-order_server-' +dataList["id"]+'">'+dataList["detail"]["server"][0].substring(-1,10)+'...</a></td>' +
			  	 '<td class="col-md-1 col-sm-12 col-xs-12">'+ dataList["order_mark"] +'</td>' +
		  	 '</tr>' +		    				
			'</table>' +
		'</div>'; 	

		return '<div class="row">'+ downloadHtml + '</div>';
	    	    						
	default:
		var serviceHtml = '<div class="col-md-12 col-sm-12 col-xs-12">' +
		'<legend>工单明细</legend>' +
			'<table class="table table-striped" cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">'+ 
			'<tr>' +
				'<th>工单内容</th>' +
				'<th>工单文件</th>' +
				'<th>文件类型</th>' +
				'<th>md5值</th>' +
				'<th>最后修改时间</th>' +
			'</tr>' + 
			'</tr>' + 
			  	 '<td class="col-md-1 col-sm-12 col-xs-12"><a data-toggle="modal" id="tooltips-order_content-'+dataList["id"]+'">'+dataList["detail"]["order_content"].substring(-1,10)+'...</a></td>' +
			  	 '<td class="col-md-1 col-sm-12 col-xs-12"><a data-toggle="modal" id="tooltips-order_server-' +dataList["id"]+'">'+dataList["detail"]["file_path"]+'</a></td>' +
			  	 '<td class="col-md-1 col-sm-12 col-xs-12">'+ dataList["detail"]["file_type"] +'</td>' +
			  	 '<td class="col-md-1 col-sm-12 col-xs-12">'+ dataList["detail"]["file_md5"] +'</td>' +
			  	'<td class="col-md-1 col-sm-12 col-xs-12">'+ dataList["detail"]["modify_time"] +'</td>' +
		  	 '</tr>' +		    				
			'</table>' +
		'</div>'; 		
		return '<div class="row">'+ serviceHtml + '</div>';		
	}	
				
}

function taskInfoFormat(dataList){
	if (dataList["file"]){
		var download = '<td class="col-md-1 col-sm-12 col-xs-12"><div class="btn-group  btn-group-xs"><button type="button" name="btn-task-file" onclick="downLoadTaskFiles(this,\'' +dataList["id"]+'\')" value="'+ dataList["id"] +'" class="btn btn-default" title="下载" aria-label="Justify"><span class="fa fa-cloud-download" aria-hidden="true"></span></button></div></td>'
	}else{
		var download = '<td class="col-md-1 col-sm-12 col-xs-12"></td>'
	}
	var taskHtml = '<div class="col-md-12 col-sm-12 col-xs-12">' +
	'<legend>任务明细</legend>' +
		'<table class="table table-striped" cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">'+ 
		'<tr>' +
			'<th>任务文件</th>' +
			'<th>下载文件</th>' +
			'<th>失败原因</th>' +
		'</tr>' + 
		'</tr>' + 
		  	 '<td class="col-md-1 col-sm-12 col-xs-12">'+ dataList["file"] + '</td>' +
		  	 	download +
		  	 '<td class="col-md-1 col-sm-12 col-xs-12">'+ dataList["msg"] +'</td>' +
	  	 '</tr>' +		    				
		'</table>' +
	'</div>'; 		
	return '<div class="row">'+ taskHtml + '</div>';		
}

function downLoadTaskFiles(obj,id){
	$("button[name='btn-task-file']").attr("disabled",true);
    downLoadFile({ //调用下载方法
    			url:"/api/account/user/task/"+ id +"/download/"
	        	}); 
    $("button[name='btn-task-file']").attr("disabled",false);
}

function InitDataConfigTable(tableId,url,buttons,columns,columnDefs){
	  var data = requests('get',url)
	  oOverviewTable =$('#'+tableId).dataTable(
			  {
				    "dom": "Bfrtip",
				    "buttons":buttons,
		    		"bScrollCollapse": false, 				
		    	    "bRetrieve": true,			
		    		"destroy": true, 
		    		"data":	data,
		    		"columns": columns,
		    		"columnDefs" :columnDefs,			  
		    		"language" : language,
		    		"order": [[ 0, "ase" ]],
		    		"autoWidth": false	    			
		    	});
}

function RefreshConfigTable(tableId, urlData){
	$.getJSON(urlData, null, function( dataList )
	{
	  table = $('#'+tableId).dataTable();
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

function makeOrderLogsTableList(url){
	if ($('#ordersLogs').hasClass('dataTable')) {
		dttable = $('#ordersLogs').dataTable();
		dttable.fnClearTable(); //清空table
		dttable.fnDestroy(); //还原初始化datatable
	}	
	var data = requests('get',url)
    var columns = [		                   
                    {"data": "order"},
                    {"data": "operator"},
                    {"data": "operation_info"},
                    {"data": "audit_status"},
                    {"data": "execute_status"},
	                {"data": "operation_time"}			                			                
	               ]
    var columnDefs = [			                      
						{
							targets: [3],
							render: function(data, type, row, meta) {
						        return orderAuditStatusHtml[row.audit_status]
							},
						},
						{
							targets: [4],
							render: function(data, type, row, meta) {
						        return orderExecuteStatusHtml[row.execute_status]
							},
						}						
	    		      ]
    
    var buttons = [
			    					    
    ] 		    
    $('#ordersLogs').dataTable({
	    "dom": "Bfrtip",
	    "buttons":buttons,
		"bScrollCollapse": false, 				
	    "bRetrieve": true,			
		"destroy": true, 
		"data":	data,
		"columns": columns,
		"columnDefs" :columnDefs,			  
		"language" : language,
		"order": [[ 0, "desc" ]],
		"autoWidth": false	    			
	});    
}