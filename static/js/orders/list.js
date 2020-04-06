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

function DynamicSelect(ids,value){
	$("#" + ids +" option").each(function(){ 
		$(this).prop("selected",false);   
	})
	$("#" + ids +" option[value='" + value +"']").prop("selected",true);	
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


function InitDataTable(tableId,url,buttons,columns,columnDefs){
	  var data = requests('get',url)
	  oOverviewTable =$('#'+tableId).dataTable({
				    "dom": "Bfrtip",
				    "buttons":buttons,
		    		"bScrollCollapse": false, 				
		    	    "bRetrieve": true,			
		    		"destroy": true, 
		    		"data":	data["results"],
		    		"columns": columns,
		    		"columnDefs" :columnDefs,			  
		    		"language" : language,
		    		"order": [[ 0, "ase" ]],
		    		"autoWidth": false	    			
	  });
	  if (data['next']){
		  $("button[name='page_next']").attr("disabled", false).val(data['next']);	
	  }else{
		  $("button[name='page_next']").attr("disabled", true).val();
	  }
	  if (data['previous']){
		  $("button[name='page_previous']").attr("disabled", false).val(data['next']);	
	  }else{
		  $("button[name='page_previous']").attr("disabled", true).val();
	  }	  

}

function RefreshOrdersTable(tableId, urlData){
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
    InitDataConfigTable('ordersLogs',url,buttons,columns,columnDefs);   		
}

$(document).ready(function() {
	
	$("button[name='noticeonfig']").on("click", function(){
		var vIds = $(this).val();
		if (vIds > 0){
			$.ajax({
				dataType: "JSON",
				url:'/api/orders/notice/'+vIds+'/', //请求地址
				type:"PUT",  //提交类似
				data:{
					"order_type":$('#order_type option:selected').val(),
					"mode":$('#mode option:selected').val(),
					"number":$("#number").val()
				}, //提交参数
				success:function(response){
	            	new PNotify({
	                    title: 'Success!',
	                    text: '修改成功',
	                    type: 'success',
	                    styling: 'bootstrap3'
	                });   
	            	RefreshConfigTable('configList', '/api/orders/notice/')
				
				},
		    	error:function(response){
	            	new PNotify({
	                    title: 'Ops Failed!',
	                    text: response.responseText,
	                    type: 'error',
	                    styling: 'bootstrap3'
	                });  
		    	}
			})			
		}else{
			$.ajax({
				dataType: "JSON",
				url:'/api/orders/notice/', //请求地址
				type:"POST",  //提交类似
				data:$("#order_config").serialize(), //提交参数
				success:function(response){
	            	new PNotify({
	                    title: 'Success!',
	                    text: '添加成功',
	                    type: 'success',
	                    styling: 'bootstrap3'
	                });   
	            	RefreshConfigTable('configList', '/api/orders/notice/')
				
				},
		    	error:function(response){
	            	new PNotify({
	                    title: 'Ops Failed!',
	                    text: response.responseText,
	                    type: 'error',
	                    styling: 'bootstrap3'
	                });  
		    	}
			})				
		}
	})
	
	function makeConfigList(){
	    var columns = [
	                   	{"data": "id","className": "text-center",},
	                    {"data": "order_type","className": "text-center",},	
	                    {"data": "mode","className": "text-center",},
/*	                    {"data": "number","className": "text-center",},*/
		               ]
	    var columnDefs = [		
	   	    		    {
	    	    				targets: [1],
	    	    				render: function(data, type, row, meta) {		    	    					
	    	    					return orderTypeHtml[row.order_type]
	    	    				},
	    	    				"className": "text-center",
   	    		        },	    
   	    		        {
    	    				targets: [2],
    	    				render: function(data, type, row, meta) {		    	    					
    	    					return '<strong>'+orderMode[row.mode]+'</strong>'
    	    				},
    	    				"className": "text-center",
	    		        },  	    		        
   	    		        {
	    	    				targets: [3],
	    	    				render: function(data, type, row, meta) {		    	    					
	    	                        return '<div class="btn-group  btn-group-xs">' +	
		    	                           '<button type="button" name="btn-config-edit" value="'+ row.id +'" class="btn btn-default"  aria-label="Justify"><span class="fa fa-edit" aria-hidden="true"></span>' +	
		    	                           '</button>' +                 				                            		                            			                          
		    	                           '<button type="button" name="btn-config-delete" value="'+ row.id +'" class="btn btn-default" aria-label="Justify"><span class="fa fa-trash" aria-hidden="true"></span>' +	
		    	                           '</button>' +			                            
		    	                           '</div>';
	    	    				},
	    	    				"className": "text-center",
   	    		        },
   	    		      ]	
        var buttons = [{
            text: '<span class="fa fa-plus"></span>',
            className: "btn-xs",
            action: function ( e, dt, node, config ) {
            	addCategory()
            }
        }]
		InitDataConfigTable('configList',"/api/orders/notice/",buttons,columns,columnDefs)
	}	  
	makeConfigList()	
	
    $('#configList tbody').on('click',"button[name='btn-config-edit']", function(){
    	var vIds = $(this).val();    	
		$.ajax({
			dataType: "JSON",
			url:'/api/orders/notice/'+vIds+'/', //请求地址
			type:"GET",  //提交类似
			success:function(response){
				DynamicSelect("order_type",response["order_type"])	
				$("#order_type").prop('disabled', true);
				DynamicSelect("grant_group",response["grant_group"])	
				DynamicSelect("mode",response["mode"])
				$("#number").val(response["number"])
				$('.selectpicker').selectpicker('refresh');	
				$("button[name='noticeonfig']").val(vIds).text("修改")
			},
	    	error:function(response){
            	new PNotify({
                    title: 'Ops Failed!',
                    text: response.responseText,
                    type: 'error',
                    styling: 'bootstrap3'
                });  
	    	}
		})    	
    })	

    $('#configList tbody').on('click',"button[name='btn-config-delete']", function(){
    	var vIds = $(this).val();
    	var td = $(this).parent().parent().parent().find("td")
    	var name = td.eq(1).text(); 
    	var mode = td.eq(2).text();
		$.confirm({
		    title: '删除确认',
		    content: "确认删除:【"+ name +"】使用<strong>"+mode+"</strong>发送通知方式？",
		    type: 'red',
		    buttons: {
		        删除: function () {
		    	$.ajax({  
		            type: "DELETE",  
		            url:'/api/orders/notice/'+vIds+'/',  
		            error: function(response) {  
		            	new PNotify({
		                    title: 'Ops Failed!',
		                    text: "删除失败",
		                    type: 'error',
		                    styling: 'bootstrap3'
		                });       
		            },  
		            success: function(response) {  
		            	new PNotify({
		                    title: 'Success!',
		                    text: "删除成功",
		                    type: 'success',
		                    styling: 'bootstrap3'
		                });	
		            	RefreshConfigTable('configList', '/api/orders/notice/')
		            }  
		    	});
		        },
		        取消: function () {
		            return true;			            
		        },			        
		    }
		}) 	
    })  	
	
	
	var userList = requests("get","/api/account/user/")
	for (var i=0; i <userList.length; i++){
		userInfo[userList[i]["id"]] = userList[i]
	}
    if ($("#ordersLists").length) {
    	
        $("button[name^='page_']").on("click", function(){
          	var url = $(this).val();
          	$(this).attr("disabled",true);
          	if (url.length){
          		RefreshOrdersTable('ordersLists', url);
          	}      	
        	$(this).attr('disabled',false);
          }); 
    	
    	var currentUser = $("#currentUser").val()
    	
    	function makeOrderTableList(){
		    var columns = [
		                   	{
		                   		"className":      'details-control',
			                    "orderable":      false,
			                    "data":           null,
			                    "defaultContent": ''
			                },		                   
		                    {"data": "id"},
		                    {"data": "order_type"},
		                    {"data": "order_user"},
			                {"data": "order_subject"},
			                {"data": "order_executor"},	
			                {"data": "create_time"},	
			                {"data": "order_execute_status","className": "text-center",},
			                {"data": "order_audit_status","className": "text-center",},	
			                {"data": "expire","className": "text-center",},	
			                {"data": "end_time"},			                			                
			               ]
		    var columnDefs = [			                      
								{
									targets: [2],
									render: function(data, type, row, meta) {
										return orderTypeHtml[row.order_type]
									},
								},
								{
									targets: [3],
									render: function(data, type, row, meta) {
								        return userInfo[row.order_user]["name"]
									},
								},
								{
									targets: [5],
									render: function(data, type, row, meta) {
								        return userInfo[row.order_executor]["name"]
									},
								},	
								{
									targets: [7],
									render: function(data, type, row, meta) {
								        return orderExecuteStatusHtml[row.order_execute_status]
									},
								},									
								{
									targets: [8],
									render: function(data, type, row, meta) {
								        return orderAuditStatusHtml[row.order_audit_status]
									},
								},		
								{
									targets: [9],
									render: function(data, type, row, meta) {
										switch(row.expire){
										case 1:
											return '<span class="label label-success">未过期</span>'
										case 2:
											return '<span class="label label-warning">未到期</span>'											
										default:
											return '<span class="label label-danger">已过期</span>'
										}
									},
								},								
	    	    		        {
		    	    				targets: [11],
		    	    				render: function(data, type, row, meta) {	
		    	    					if (currentUser==row.order_executor || userInfo[currentUser]["is_superuser"]){
		    	    						/*如果是工单完成人或者超级管理员授权*/
		    	    						var grant = '<button type="button" name="btn-order-grant" value="'+ row.id + ':' + row.order_audit_status  +'" class="btn btn-default"  aria-label="Justify"><span class="fa fa-check" aria-hidden="true"></span></button>'
		    	    					}else{
		    	    						var grant = ''
		    	    					}		    	    					
		    	    					if (userInfo[currentUser]["is_superuser"]){
		    	    						/*如果是运维服务工单已授权，*/
		    	    						var edit = '<button type="button" name="btn-order-edit" value="'+ row.id + ':' + row.order_execute_status  +'" class="btn btn-default"  aria-label="Justify"><span class="fa fa-edit" aria-hidden="true"></span></button>'
		    	    					}else{
		    	    						var edit = ''
		    	    					}
		    	    					/*----------*/
		    	    					switch(row.order_type)
		    	    					{
		    	    					case 0:
		    	    						var url = '/order/sql/handle/?id='+row.id
		    	    					  break;
		    	    					case 2:
		    	    						var url = '/order/fileupload/handle/?id='+row.id
		    	    					  break;
		    	    					case 3:
		    	    						var url = '/order/filedownload/handle/?id='+row.id
		    	    					  break;		    	    						
		    	    					default:
		    	    						var url = '/order/service/handle/?id='+row.id
		    	    					}
		    	                        return '<div class="btn-group  btn-group-sm">' +	
			    	                           '<button type="button" name="btn-order-run" value="'+ row.id +'" class="btn btn-default"  aria-label="Justify"><a href="'+url+'"><span class="glyphicon glyphicon-play-circle" aria-hidden="true"></span></a>' +	
			    	                           '</button>' + grant + edit + 	
			    	                           '<button type="button" name="btn-order-log" value="'+ row.id +'" class="btn btn-default"  aria-label="Justify" data-toggle="modal" data-target=".bs-example-modal-log"><span class="fa fa-search-plus" aria-hidden="true"></span></button>'
			    	                           '</div>';
		    	    				},
		    	    				"className": "text-center",
	    	    		        },
	    	    		      ]
		    
		    var buttons = [
						    {
						        text: '<span class="fa fa-cogs"></span>',
						        className: "btn-sm",
						        action: function ( e, dt, node, config ) {        	
		    	                    if($('#noticeConfigDiv').is(':hidden')){
		    	                    	$('#noticeConfigDiv').show();
		    	                    }
		    	                    else{
		    	                    	$('#noticeConfigDiv').hide();
		    	                    } 						        	
						        }
						    },		                   
		                   {
					        text: '<span class="fa fa-cubes"></span>',
					        className: "btn-sm",
					        action: function ( e, dt, node, config ) { 
					        	window.open('/order/apply/')
					        }
					    },
					    {
					        text: '<span class="fa fa-cloud-upload"></span>',
					        className: "btn-sm",
					        action: function ( e, dt, node, config ) {        	
					        	window.open('/order/apply/')
					        }
					    },	
					    {
					        text: '<span class="fa fa-cloud-download"></span>',
					        className: "btn-sm",
					        action: function ( e, dt, node, config ) {        	
					        	window.open('/order/apply/')
					        }
					    },						    
					    
		    ] 		    
		    InitDataTable('ordersLists','/api/orders/list/',buttons,columns,columnDefs);   		
    	}
    	
    	makeOrderTableList()
    	
    	var table = $('#ordersLists').DataTable();
    	
    	$('#ordersLists tbody').on('click', 'td.details-control', function () {
	    	var dataList = [];
	        var tr = $(this).closest('tr');
	        var row = table.row( tr );	        
	        aId = row.data()["id"];
	        order_type = row.data()["order_type"]
	        $.ajax({
//	            url : "/order/info/?type="+ orderTypeJson[order_type] +"&&id="+aId,
	        	url: "/api/orders/"+ aId +"/",
	            type : "get",
	            async : false,
	            success : function(result) {
	            	dataList = result;
	            }
	        });	        
	        if ( row.child.isShown() ) {
	            row.child.hide();
	            tr.removeClass('shown');
	        }
	        else {
	            row.child( orderInfoFormat(dataList) ).show();
	            tr.addClass('shown');
	        }
	        switch(order_type)
	        {
	        case 0:
		        $('#tooltips-sql-'+aId).pt({
		            position: 'r', // 默认属性值
		            align: 'c',	   // 默认属性值
		            height: 'auto',
		            width: 'auto',
		            content: dataList["detail"]["order_sql"].replace(/;/g, ";<br>") 
		        }); 
		        $('#tooltips-err-'+aId).pt({
		            position: 'r', // 默认属性值
		            align: 'c',	   // 默认属性值
		            height: 'auto',
		            width: 'auto',
		            content: dataList["detail"]["order_err"].replace(/;/g, ";<br>") 
		        });
	          break;
	        case 1:
		        $('#tooltips-order_content-'+aId).pt({
		            position: 'r', // 默认属性值
		            align: 'c',	   // 默认属性值
		            height: 'auto',
		            width: 'auto',
		            content: dataList["detail"]["order_content"]
		        });	
	          break;	          
	        case 2:
	        	var server = ''
	        	for (var i=0; i <dataList["detail"]["server"].length; i++){
	        		server += dataList["detail"]["server"][i] + ';'
	        	}
		        $('#tooltips-order_content-'+aId).pt({
		            position: 'r', // 默认属性值
		            align: 'c',	   // 默认属性值
		            height: 'auto',
		            width: 'auto',
		            content: dataList["detail"]["order_content"]
		        });	
		        $('#tooltips-order_server-'+aId).pt({
		            position: 'r', // 默认属性值
		            align: 'c',	   // 默认属性值
		            height: 'auto',
		            width: 'auto',
		            content: server.replace(/;/g, "<br>") 
		        });	        
	          break;
	        case 3:
	        	var server = ''
		        	for (var i=0; i <dataList["detail"]["server"].length; i++){
		        		server += dataList["detail"]["server"][i] + ';'
		        	}
			        $('#tooltips-order_content-'+aId).pt({
			            position: 'r', // 默认属性值
			            align: 'c',	   // 默认属性值
			            height: 'auto',
			            width: 'auto',
			            content: dataList["detail"]["order_content"]
			        });	
			        $('#tooltips-order_server-'+aId).pt({
			            position: 'r', // 默认属性值
			            align: 'c',	   // 默认属性值
			            height: 'auto',
			            width: 'auto',
			            content: server.replace(/;/g, "<br>") 
			        });	 	        	
	          break;
	        default:
	          break;
	        }         
	    });	
    	 
    	
    	$('#ordersLists tbody').on('click','button[name="btn-order-grant"]',function(){
    		var vIds = $(this).val().split(":");
    		let orderInfo = $(this).parent().parent().parent().find("td")
    		let username =  orderInfo.eq(3).text()
    		let order_subject = orderInfo.eq(4).text()
    	    $.confirm({
    	        icon: 'fa fa-check',
    	        type: 'blue',
    	        title: '修改<code>'+username+'</code>申请的<strong>《'+ order_subject  + '》</strong>工单审核状态?',
    	        content: '<form  data-parsley-validate class="form-horizontal form-label-left">' +
				            '<div class="form-group">' +
				              '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">工单状态<span class="required">*</span>' +
				              '</label>' +
				              '<div class="col-md-6 col-sm-6 col-xs-12">' +
				              			makeOrderAuditStatusSelect(parseInt(vIds[1])) +
				              '</div>' +
				            '</div>' + 
					        '<div class="form-group">' +
					        '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">审批建议: <span class="required">*</span>' +
					        '</label>' +
					        '<div class="col-md-6 col-sm-6 col-xs-12">' +
					          '<input type="text"  name="order_mark" class="form-control col-md-7 col-xs-12">' +
					        '</div>' +				            
				          '</form>',
    	        buttons: {
    	            '取消': function() {},
    	            '确认': {
    	                btnClass: 'btn-blue',
    	                action: function() {
    	                	var formData = {};	
    	            		var vipForm = this.$content.find('select,input');                	
    	            		for (var i = 0; i < vipForm.length; ++i) {
    	            			var name =  vipForm[i].name
    	            			var value = vipForm[i].value 
    	            			if (name.length >0 && value.length > 0){
    	            				formData[name] = value	
    	            			};		            						
    	            		};	    	                	
    				    	$.ajax({  
    				            cache: true,  
    				            type: "PUT",  
    				            url:"/api/orders/" + vIds[0] + '/',  
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
    				                    text: '工单授权成功',
    				                    type: 'success',
    				                    styling: 'bootstrap3'
    				                }); 
    				            	/*RefreshDeployRolesTable("#deployRolesList","/apps/config/?type=info&id="+get_url_param('id'))*/
    				            	RefreshOrdersTable('ordersLists','/api/orders/list/')
    				            }  
    				    	});
    	                }
    	            }
    	        }
    	    });     		
    	});	  
    	
    	$('#ordersLists tbody').on('click','button[name="btn-order-edit"]',function(){
    		var vIds = $(this).val().split(":");
    		let orderInfo = $(this).parent().parent().parent().find("td")
    		let username =  orderInfo.eq(3).text()
    		let order_subject = orderInfo.eq(4).text()
    	    $.confirm({
    	        icon: 'fa fa-check',
    	        type: 'blue',
    	        title: '修改<code>'+username+'</code>申请的<strong>《'+ order_subject  + '》</strong>工单进度?',
    	        content: '<form  data-parsley-validate class="form-horizontal form-label-left">' +
				            '<div class="form-group">' +
				              '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">工单进度<span class="required">*</span>' +
				              '</label>' +
				              '<div class="col-md-6 col-sm-6 col-xs-12">' +
				              		 makeOrderExecuteStatusSelect(parseInt(vIds[1])) +
				              '</div>' +
				            '</div>' + 
					        '<div class="form-group">' +
					        '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">处理建议: <span class="required">*</span>' +
					        '</label>' +
					        '<div class="col-md-6 col-sm-6 col-xs-12">' +
					          '<input type="text"  name="order_mark"  class="form-control col-md-7 col-xs-12">' +
					        '</div>' +				            
				          '</form>',
    	        buttons: {
    	            '取消': function() {},
    	            '确认': {
    	                btnClass: 'btn-blue',
    	                action: function() {
    	                	var formData = {};	
    	            		var vipForm = this.$content.find('select,input');                	
    	            		for (var i = 0; i < vipForm.length; ++i) {
    	            			var name =  vipForm[i].name
    	            			var value = vipForm[i].value 
    	            			if (name.length >0 && value.length > 0){
    	            				formData[name] = value	
    	            			};		            						
    	            		};	    	                	
    				    	$.ajax({  
    				            cache: true,  
    				            type: "PUT",  
    				            url:"/api/orders/" + vIds[0] + '/',  
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
    				                    text: '工单授权成功',
    				                    type: 'success',
    				                    styling: 'bootstrap3'
    				                }); 
    				            	/*RefreshDeployRolesTable("#deployRolesList","/apps/config/?type=info&id="+get_url_param('id'))*/
    				            	RefreshOrdersTable('ordersLists','/api/orders/list/')
    				            }  
    				    	});
    	                }
    	            }
    	        }
    	    });     		
    	});	 
    	
    	$('#ordersLists tbody').on('click','button[name="btn-order-log"]',function(){
    		var vIds = $(this).val();
    		orderInfo = $(this).parent().parent().parent().find("td")
    		order_subject = orderInfo.eq(4).text()
    		$("#orderLogModalLabel").text(order_subject)
    		if ($('#ordersLogs').hasClass('dataTable')) {
    			dttable = $('#ordersLogs').dataTable();
    			dttable.fnClearTable(); //清空table
    			dttable.fnDestroy(); //还原初始化datatable
    		}	    		
    		makeOrderLogsTableList("/api/orders/logs/"+ vIds +"/")
    	});    	
    	
	}
    
	
})